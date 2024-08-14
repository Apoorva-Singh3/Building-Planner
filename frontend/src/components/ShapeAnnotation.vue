<template>
    <div :style="annotationStyle" class="annotation">{{ annotation.text }}</div>
  </template>
  
  <script>
  export default {
    props: {
      annotation: Object,
    },
    computed: {
      annotationStyle() {
        const { x, y } = this.annotation.position;
        return {
          position: 'absolute',
          left: `${x}px`,
          top: `${y}px`,
          backgroundColor: 'yellow',
          padding: '2px 4px',
          border: '1px solid #000',
          borderRadius: '3px',
          fontSize: '12px',
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .annotation {
    cursor: pointer;
  }
  </style>
  