<template>
    <div class="toolbar">
      <button @click="selectTool('draw', 'line')">Draw Line</button>
      <button @click="selectTool('draw', 'rectangle')">Draw Rectangle</button>
      <button @click="selectTool('draw', 'circle')">Draw Circle</button>
      <button @click="selectTool('select')">Select</button>
      <button @click="toggleAnnotations">View Annotations</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      selectTool(tool, shapeType = null) {
        this.$emit('tool-selected', { tool, shapeType });
      },
      toggleAnnotations() {
        this.$emit('toggle-annotations');
      },
    },
  };
  </script>
  
  <style scoped>
  .toolbar {
    display: flex;
    justify-content: space-around;
    margin-bottom: 10px;
  }
  </style>
  