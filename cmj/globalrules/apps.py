from django import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.management import _get_all_permissions
from django.core import exceptions
from django.db import models, router
from django.db.utils import DEFAULT_DB_ALIAS
from django.utils.translation import ugettext_lazy as _, string_concat


class AppConfig(apps.AppConfig):
    name = 'cmj.globalrules'
    label = 'globalrules'
    verbose_name = _('Regras e Permissões para o Portal')


def create_proxy_permissions(
        app_config, verbosity=2, interactive=True,
        using=DEFAULT_DB_ALIAS, **kwargs):
    if not app_config.models_module:
        return

    # print(app_config)

    try:
        Permission = apps.get_model('auth', 'Permission')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Permission):
        return

    from django.contrib.contenttypes.models import ContentType

    permission_name_max_length = Permission._meta.get_field('name').max_length

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in list(app_config.get_models()):
        opts = klass._meta
        permissions = (
            ("list_" + opts.model_name,
             string_concat(
                 _('Visualizaçao da lista de'), ' ',
                 opts.verbose_name_plural)),
            ("detail_" + opts.model_name,
             string_concat(
                 _('Visualização dos detalhes de'), ' ',
                 opts.verbose_name_plural)),
        )
        opts.permissions = tuple(
            set(list(permissions) + list(opts.permissions)))

        if opts.proxy:
            # Force looking up the content types in the current database
            # before creating foreign keys to them.
            app_label, model = opts.app_label, opts.model_name

            try:
                ctype = ContentType.objects.db_manager(
                    using).get_by_natural_key(app_label, model)
            except:
                ctype = ContentType.objects.db_manager(
                    using).create(app_label=app_label, model=model)
        else:
            ctype = ContentType.objects.db_manager(using).get_for_model(klass)

        ctypes.add(ctype)
        for perm in _get_all_permissions(klass._meta, ctype):
            searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(Permission.objects.using(using).filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    perms = [
        Permission(codename=codename, name=name, content_type=ct)
        for ct, (codename, name) in searched_perms
        if (ct.pk, codename) not in all_perms
    ]
    # Validate the permissions before bulk_creation to avoid cryptic database
    # error when the name is longer than 255 characters
    for perm in perms:
        if len(perm.name) > permission_name_max_length:
            raise exceptions.ValidationError(
                'The permission name %s of %s.%s '
                'is longer than %s characters' % (
                    perm.name,
                    perm.content_type.app_label,
                    perm.content_type.model,
                    permission_name_max_length,
                )
            )
    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)


def update_groups_cmj(app_config, verbosity=2, interactive=True,
                      using=DEFAULT_DB_ALIAS, **kwargs):

    if app_config != AppConfig and not isinstance(app_config, AppConfig):
        return

    from cmj.globalrules.map_rules import rules_patterns
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    class Rules:

        def __init__(self, rules_patterns):
            self.rules_patterns = rules_patterns

        def associar(self, g, model, tipo):
            for t in tipo:
                content_type = ContentType.objects.get_by_natural_key(
                    app_label=model._meta.app_label,
                    model=model._meta.model_name)

                codename = (t[1:] + model._meta.model_name)\
                    if t[0] == '.' and t[-1] == '_' else t

                p = Permission.objects.get(
                    content_type=content_type,
                    codename=codename)
                g.permissions.add(p)
            g.save()

        def _config_group(self, group_name, rules_list):
            if not group_name:
                return

            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()

            try:
                print(' ', group_name)
                for model, perms in rules_list:
                    self.associar(group, model, perms)
            except Exception as e:
                print(group_name, e)

        def update_groups(self):
            print('')
            print(string_concat('\033[93m\033[1m',
                                _('Atualizando grupos do Portal CMJ:'),
                                '\033[0m'))
            for rules_group in self.rules_patterns:
                group_name = rules_group['group']
                rules_list = rules_group['rules']
                self._config_group(group_name, rules_list)

    rules = Rules(rules_patterns)
    rules.update_groups()


models.signals.post_migrate.connect(
    receiver=update_groups_cmj)


models.signals.post_migrate.connect(
    receiver=create_proxy_permissions,
    dispatch_uid="django.contrib.auth.management.create_permissions")
