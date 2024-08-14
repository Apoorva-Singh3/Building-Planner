<template>
    <div :style="shapeStyle" 
         @mousedown="selectShape" 
         class="shape">
      <div v-if="isSelected" 
           class="resize-handle" 
           :style="handleStyle" 
           @mousedown.stop="startResizing"></div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      shape: Object,
      isSelected: Boolean,
    },
    computed: {
      shapeStyle() {
        const { x1, y1, x2, y2 } = this.shape.coordinates;
        const width = Math.abs(x2 - x1);
        const height = Math.abs(y2 - y1);
        const left = Math.min(x1, x2);
        const top = Math.min(y1, y2);
        return {
          position: 'absolute',
          left: `${left}px`,
          top: `${top}px`,
          width: `${width}px`,
          height: `${height}px`,
          border: this.shape.type === 'line' ? '1px solid black' : '2px solid black',
          backgroundColor: this.shape.type !== 'line' ? '#ddd' : 'transparent',
          cursor: 'move',
        };
      },
      handleStyle() {
        return {
          position: 'absolute',
          right: '-5px',
          bottom: '-5px',
          width: '10px',
          height: '10px',
          backgroundColor: 'blue',
          cursor: 'nwse-resize',
        };
      },
    },
    methods: {
      // selectShape(event) {
      //   this.$emit('select', this.shape);
      // },
      startResizing(event) {
        event.stopPropagation();
        this.$emit('resize', event);
      },
    },
  };
  </script>
  
  <style scoped>
  .shape {
    transition: border-color 0.3s;
  }
  
  .shape:hover {
    border-color: #000;
  }
  
  .resize-handle {
    background-color: blue;
    border-radius: 50%;
  }
  </style>
  