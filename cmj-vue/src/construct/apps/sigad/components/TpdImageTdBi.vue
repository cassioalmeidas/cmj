<template lang="html">
  <div :class="[name_component, 'draggable', classDrag]"
    v-on:dragend="dragend"
    v-on:dragenter="dragenter"
    v-on:dragleave="dragleave"
    v-on:dragover="dragover"
    v-on:dragstart="dragstart"
    v-on:dragexit="dragexit"
    v-on:drop="drop"
    v-on:mouseover="mouseOver"
    v-on:mouseleave="mouseLeave">
      <img :src="slug+'.128?'+refresh">
      <div class="drag" @click="$emit('showmodal', elemento, pos)"></div>
      <div class="imgmouseover" v-if="mouseover">
        <img :src="slug+'.512?'+refresh">
      </div>
  </div>
</template>

<script>
import Container from './Container'

export default {
  name: 'tpd-image-td-bi',
  props: ['pos'],
  extends: {
    ...Container
  },
  data () {
    return {
      dragged: false,
      draggedover: 0,
      draggedleave: false,
      mouseover: false
    }
  },
  computed: {
    classDrag: function () {
      let classes = Array() //eslint-disable-line
      this.dragged ? classes.push('drag-start') : '' //eslint-disable-line
      this.draggedleave ? classes.push('drag-leave') : '' //eslint-disable-line
      this.draggedover !== 0 ? classes.push('drag-over') : '' //eslint-disable-line
      return classes
    }
  },
  methods: {
    mouseOver (ev) {
      this.mouseover = true
    },
    mouseLeave (ev) {
      this.mouseover = false
    },
    dragend (ev) {
      console.log('dragend: tpdimagetdbi', ev)
      if (this.dragged) {
        this.$emit('ondragend', this.elemento)
      }
      this.dragged = false
      this.draggedleave = false
      this.draggedover = 0
    },
    dragenter (ev) {
      console.log('dragenter: tpdimagetdbi', ev)
      if (this.dragged) {
        this.draggedleave = false // não deve ser atribuido true em caso contrário
      }
    },
    dragleave (ev) {
      console.log('dragleave: tpdimagetdbi', ev)
      this.$emit('ondragleave', this.elemento, this.draggedover)
      this.draggedleave = this.dragged
      this.draggedover = 0
    },
    dragover (ev) {
      console.log('dragover: tpdimagetdbi', ev)
      if (!this.dragged) {
        this.draggedover = ev.offsetX - ev.target.offsetWidth / 2
      }
    },
    dragstart (ev) {
      console.log('dragstart: tpdimagetdbi', ev)
      this.dragged = true
    },
    dragexit (ev) {
      console.log('dragexit: tpdimagetdbi', ev)
    },
    drop (ev) {
      console.log('drop: tpdimagetdbi', ev)
    }
  }
}
</script>

<style lang="scss">
.container-documento-edit {
  .tpd-image-td-bi {
    flex: 0 1 auto;
    flex-direction: row;
    padding: 5px;
    opacity: 0.8;
    transition: all 1s ease;
    margin:2px;
    position: relative;
    user-select:none;
    width: auto;
    &:hover {
      transition: all 0.3s ease;
      opacity: 1;
    }

    &.drag-start {
      opacity: 0.5;
      transition: all 1s ease;
    }
    &.drag-leave {
      opacity: 0.1;
      transition: all 1s ease;
    }
    &.drag-over {
      opacity: 0.2;
      transition: all 1s ease;
    }
    .drag {
      border: 1px solid #aaa;
      position: absolute;
      top: 0;
      left:0;
      right: 0;
      bottom: 0;
      display: block;

      -moz-user-select: none;
      -khtml-user-select: none;
      -webkit-user-select: none;
      user-select: none;
      -khtml-user-drag: element;
      -webkit-user-drag: element;
    }

    .imgmouseover {
      position: absolute;
      z-index: 2001;
      background: white;
      padding: 10px;
      box-shadow: 0px 0px 6px white;
      top:90%;
      left: 10px;
      border: 1px solid #fafafa;

    }

  }
}
</style>
