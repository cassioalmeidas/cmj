
from compressor.utils.decorators import cached_property
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import permalink
from django.db.models.deletion import PROTECT, CASCADE
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField
from sapl.parlamentares.models import Municipio, Parlamentar

from cmj.core.rules import SEARCH_TRECHO
from cmj.globalrules.globalrules import rules, GROUP_SOCIAL_USERS
from cmj.utils import get_settings_auth_user_model, normalize, YES_NO_CHOICES

from .rules import MENU_PERMS_FOR_USERS


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,
                     email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except:
            user = self.model.objects.get_by_natural_key(email)

        rules.group_social_users_add_user(user)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


def sizeof_fmt(num, suffix='B'):
    """
    Shamelessly copied from StackOverflow:
    http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size

    :param num:
    :param suffix:
    :return:
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def avatar_validation(image):
    if image:
        # 10 MB
        max_file_size = 10 * 1024 * 1024
        if image.size > max_file_size:
            raise forms.ValidationError(
                _('The maximum file size is {0}').format(sizeof_fmt(max_file_size)))


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = ImageCropField(
        _('profile picture'), upload_to="avatars/",
        validators=[avatar_validation], null=True, blank=True)
    cropping = ImageRatioField(
        'avatar', '70x70', help_text=_(
            'Note that the preview above will only be updated after '
            'you submit the form.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta):
        abstract = False
        permissions = MENU_PERMS_FOR_USERS

    def __str__(self):
        return self.get_display_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ' '.join([self.first_name, self.last_name]).strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_display_name(self):
        return self.get_full_name() or self.email

    @permalink
    def get_absolute_url(self):
        return 'users_profile', [self.pk], {}

    def delete(self, using=None, keep_parents=False):

        if self.groups.all().exclude(name=GROUP_SOCIAL_USERS).exists():
            raise PermissionDenied(
                _('Você não possui permissão para se autoremover do Portal!'))

        return AbstractBaseUser.delete(
            self, using=using, keep_parents=keep_parents)


class CmjSearchMixin(models.Model):

    search = models.TextField(blank=True, default='')

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, auto_update_search=True):

        if auto_update_search and hasattr(self, 'fields_search'):
            search = ''
            for str_field in self.fields_search:
                fields = str_field.split('__')
                if len(fields) == 1:
                    try:
                        search += str(getattr(self, str_field)) + ' '
                    except:
                        pass
                else:
                    _self = self
                    for field in fields:
                        _self = getattr(_self, field)
                    search += str(_self) + ' '
            self.search = search
        self.search = normalize(self.search)

        return super(CmjSearchMixin, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class CmjModelMixin(models.Model):
    # para migração
    """created = models.DateTimeField(
        verbose_name=_('created'),
        editable=True, auto_now_add=False)
    modified = models.DateTimeField(
        verbose_name=_('modified'), editable=True, auto_now=False)"""
    # para produção
    created = models.DateTimeField(
        verbose_name=_('created'),
        editable=False, auto_now_add=True)
    modified = models.DateTimeField(
        verbose_name=_('modified'), editable=False, auto_now=True)

    class Meta:
        abstract = True

    def clean(self):
        """
        Check for instances with null values in unique_together fields.
        """
        from django.core.exceptions import ValidationError

        super(CmjModelMixin, self).clean()

        for field_tuple in self._meta.unique_together[:]:
            unique_filter = {}
            unique_fields = []
            null_found = False
            for field_name in field_tuple:
                field_value = getattr(self, field_name)
                if getattr(self, field_name) is None:
                    unique_filter['%s__isnull' % field_name] = True
                    null_found = True
                else:
                    unique_filter['%s' % field_name] = field_value
                    unique_fields.append(field_name)
            if null_found:
                unique_queryset = self.__class__.objects.filter(
                    **unique_filter)
                if self.pk:
                    unique_queryset = unique_queryset.exclude(pk=self.pk)
                if unique_queryset.exists():
                    msg = self.unique_error_message(
                        self.__class__, tuple(unique_fields))
                    raise ValidationError(msg)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, clean=True):
        if clean:
            self.clean()
        return models.Model.save(
            self,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)


class CmjAuditoriaModelMixin(CmjModelMixin):

    owner = models.ForeignKey(
        get_settings_auth_user_model(),
        verbose_name=_('owner'),
        related_name='+',
        on_delete=PROTECT)
    modifier = models.ForeignKey(
        get_settings_auth_user_model(),
        verbose_name=_('modifier'),
        related_name='+',
        on_delete=PROTECT)

    class Meta:
        abstract = True


class AreaTrabalho(CmjAuditoriaModelMixin):

    nome = models.CharField(max_length=100, blank=True, default='',
                            verbose_name=_('Nome'))

    descricao = models.CharField(
        default='', max_length=254, verbose_name=_('Descrição'))

    parlamentar = models.ForeignKey(
        Parlamentar,
        verbose_name=_('Parlamentar'),
        related_name='areatrabalho_set',
        blank=True, null=True, on_delete=CASCADE)

    operadores = models.ManyToManyField(
        get_settings_auth_user_model(),
        through='OperadorAreaTrabalho',
        through_fields=('areatrabalho', 'user'),
        symmetrical=False,
        related_name='areatrabalho_set')

    class Meta:
        verbose_name = _('Área de Trabalho')
        verbose_name_plural = _('Áreas de Trabalho')

    def __str__(self):
        return self.nome


class OperadorAreaTrabalho(CmjAuditoriaModelMixin):

    user = models.ForeignKey(
        get_settings_auth_user_model(),
        verbose_name=_('Operador da Área de Trabalho'),
        related_name='operadorareatrabalho_set',
        on_delete=CASCADE)

    areatrabalho = models.ForeignKey(
        AreaTrabalho,
        related_name='operadorareatrabalho_set',
        verbose_name=_('Área de Trabalho'),
        on_delete=CASCADE)

    grupos_associados = models.ManyToManyField(
        Group,
        verbose_name=_('Grupos Associados'),
        related_name='operadorareatrabalho_set')

    @property
    def user_name(self):
        return '%s - %s' % (
            self.user.get_display_name(),
            self.user.email)

    class Meta:
        verbose_name = _('Operador')
        verbose_name_plural = _('Operadores')

    def __str__(self):
        return self.user.get_display_name()


class Cep(models.Model):
    numero = models.CharField(max_length=9, verbose_name=_('CEP'), unique=True)

    class Meta:
        verbose_name = _('CEP')
        verbose_name_plural = _("CEP's")
        ordering = ('numero'),

    def __str__(self):
        return self.numero


class RegiaoMunicipal(models.Model):

    TIPO_CHOICES = [
        ('AU', _('Área Urbana')),
        ('AR', _('Área Rural')),
        ('UA', _('Área Única'))]

    nome = models.CharField(
        max_length=254, verbose_name=_('Região Municipal'))
    tipo = models.CharField(
        max_length=2,
        default='AU',
        choices=TIPO_CHOICES, verbose_name='Tipo da Região')

    class Meta:
        verbose_name = _('Região Municipal')
        verbose_name_plural = _('Regiões Municipais')
        unique_together = (
            ('nome', 'tipo'),)

    def __str__(self):
        return '%s - %s' % (
            self.nome, self.get_tipo_display())


class Distrito(models.Model):
    nome = models.CharField(
        max_length=254,
        verbose_name=_('Nome do Distrito'),
        unique=True)

    class Meta:
        verbose_name = _('Distrito')
        verbose_name_plural = _("Distritos")

    def __str__(self):
        return self.nome


class Bairro(models.Model):
    nome = models.CharField(
        max_length=254,
        verbose_name=_('Bairro'),
        unique=True)

    codigo = models.PositiveIntegerField(
        default=0,
        verbose_name='Código',
        help_text=_('Código do Bairro no Cadastro Oficial do Município'))

    outros_nomes = models.TextField(
        blank=True,
        verbose_name=_('Outros Nomes'),
        help_text=_('Ocorrências similares'))

    class Meta:
        ordering = ('nome',)
        verbose_name = _('Bairro')
        verbose_name_plural = _("Bairros")

    def __str__(self):
        return self.nome


class TipoLogradouro(models.Model):
    nome = models.CharField(
        max_length=254,
        verbose_name=_('Tipo de Logradouro'),
        unique=True)

    class Meta:
        verbose_name = _('Tipo de Logradouro')
        verbose_name_plural = _("Tipos de Logradouros")
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Logradouro(models.Model):
    nome = models.CharField(
        max_length=254,
        verbose_name=_('Logradouro'),
        unique=True)

    class Meta:
        verbose_name = _('Logradouro')
        verbose_name_plural = _("Logradouros")
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Trecho(CmjSearchMixin, CmjModelMixin):
    logradouro = models.ForeignKey(
        Logradouro,
        blank=True, null=True, default=None,
        related_name='trechos_set',
        verbose_name=_('Logradouro'))

    tipo = models.ForeignKey(
        TipoLogradouro,
        blank=True, null=True, default=None,
        related_name='trechos_set',
        verbose_name=_('Tipo de Logradouro'))

    bairro = models.ForeignKey(
        Bairro,
        blank=True, null=True, default=None,
        related_name='trechos_set',
        verbose_name=_('Bairro'))

    distrito = models.ForeignKey(
        Distrito,
        blank=True, null=True, default=None,
        related_name='trechos_set',
        verbose_name=_('Distrito'))

    regiao_municipal = models.ForeignKey(
        RegiaoMunicipal,
        blank=True, null=True, default=None,
        related_name='trechos_set',
        verbose_name=_('Região Municipal'))

    municipio = models.ForeignKey(
        Municipio,
        related_name='trechos_set',
        verbose_name=_('Município'))

    LADO_CHOICES = [
        ('NA', _('Não Aplicável')),
        ('AL', _('Ambos os Lados')),
        ('LE', _('Lado Esquerdo')),
        ('LD', _('Lado Direito'))]

    lado = models.CharField(
        max_length=2,
        default='AL',
        choices=LADO_CHOICES, verbose_name='Lado do Logradouro')

    numero_inicial = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Número Inicial')
    numero_final = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Número Final')

    # http://mundogeo.com/blog/2006/03/01/eixo-de-logradouro-conceitos-e-beneficios-parte-1/
    # Pelo que vi, os correios afirmar não haver mais de um cep por trecho,
    # portanto essa relação poderia ser 1xN, mas pra evitar contratempos
    # futuros.
    cep = models.ManyToManyField(
        Cep,
        related_name='trechos_set',
        verbose_name=_('Cep'))

    @cached_property
    def fields_search(self):
        return [
            'tipo__nome',
            'logradouro__nome',
            'bairro__nome',
            'distrito__nome',
            'regiao_municipal__nome',
            'municipio__nome',
            'cep']

    class Meta:
        verbose_name = _('Trecho de Logradouro')
        verbose_name_plural = _("Trechos de Logradouro")
        ordering = [
            'municipio__nome',
            'regiao_municipal__nome',
            'distrito__nome',
            'bairro__nome',
            'tipo__nome',
            'logradouro__nome']
        unique_together = (
            ('municipio',
                'regiao_municipal',
                'distrito',
                'bairro',
                'logradouro',
                'tipo',
                'lado',
                'numero_inicial',
                'numero_final'),)

    def __str__(self):
        uf = str(self.municipio.uf) if self.municipio else ''
        municipio = str(self.municipio.nome) + '-' if self.municipio else ''
        tipo = str(self.tipo) + ' ' if self.tipo else ''
        logradouro = str(self.logradouro) + ' - ' if self.logradouro else ''
        bairro = self.bairro.nome + ' - ' if self.bairro else ''
        distrito = self.distrito.nome + ' - ' if self.distrito else ''
        rm = self.regiao_municipal.nome + \
            ' - ' if self.regiao_municipal else ''

        join_cep = ' - '.join(self.cep.values_list('numero', flat=True))
        join_cep = ' - ' + join_cep if join_cep else ''

        return '%s%s%s%s%s%s%s%s' % (
            tipo, logradouro, bairro, distrito, rm, municipio, uf, join_cep
        )


class ImpressoEnderecamento(models.Model):
    nome = models.CharField(max_length=254, verbose_name='Nome do Impresso')

    TIPO_CHOICES = [
        ('ET', _('Folha de Etiquetas')),
        ('EV', _('Envelopes'))]

    tipo = models.CharField(
        max_length=2,
        default='ET',
        choices=TIPO_CHOICES, verbose_name='Tipo do Impresso')

    largura_pagina = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Largura da Página'),
        help_text=_('Em centímetros'))
    altura_pagina = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Altura da Página'),
        help_text=_('Em centímetros'))

    margem_esquerda = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Margem Esquerda'),
        help_text=_('Em centímetros'))
    margem_superior = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Margem Superior'),
        help_text=_('Em centímetros'))

    colunasfolha = models.PositiveSmallIntegerField(
        verbose_name=_('Colunas'))
    linhasfolha = models.PositiveSmallIntegerField(
        verbose_name=_('Linhas'))

    larguraetiqueta = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Largura da Etiqueta'),
        help_text=_('Em centímetros'))
    alturaetiqueta = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Altura da Etiquta'),
        help_text=_('Em centímetros'))

    entre_colunas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Distância Entre Colunas'),
        help_text=_('Em centímetros'))
    entre_linhas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Distância Entre Linhas'),
        help_text=_('Em centímetros'))

    fontsize = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name=_('Tamanho da Letra'),
        help_text=_('Em Pixels'))

    rotate = models.BooleanField(
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Rotacionar Texto'))

    class Meta:
        verbose_name = _('Impresso para Endereçamento')
        verbose_name_plural = _("Impressos para Endereçamento")

    def __str__(self):
        return self.nome
