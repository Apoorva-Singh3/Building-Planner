<template>
  <div id="app">
    <Toolbar @tool-selected="handleToolSelected" @toggle-annotations="toggleAnnotations" />
    <DrawingArea :selectedTool="selectedTool" 
             :selectedShapeType="selectedShapeType" 
             :drawingId="drawingId" 
             ref="drawingArea"/>

  </div>
</template>

<script>
import Toolbar from './components/DrawingToolbar.vue';
import DrawingArea from './components/DrawingArea.vue';

export default {
  components: {
    Toolbar,
    DrawingArea,
  },
  data() {
    return {
      selectedTool: 'draw',
      selectedShapeType: 'line',
      drawingId: null, // Start with null or set it dynamically
      showAnnotations: true,
    };
  },
  created() {
    // Example of setting drawingId dynamically, you could fetch it or get from route params
    // this.drawingId = this.$route.params.drawingId || null;
    this.drawingId = this.fetchDrawingId();
  
    console.log('Drawing ID:', this.drawingId);
    console.log('Selected Tool:', this.selectedTool);
    console.log('Selected Shape Type:', this.selectedShapeType);
    console.log('Drawing ID:', this.drawingId);
  },
  methods: {
    handleToolSelected({ tool, shapeType }) {
      this.selectedTool = tool;
      this.selectedShapeType = shapeType;
    },
    toggleAnnotations() {
      this.showAnnotations = !this.showAnnotations;
      this.$refs.drawingArea.toggleAnnotations();
    },
    fetchDrawingId() {
      // Example of setting drawingId based on user input or other logic
    const id = prompt('Enter drawing ID:');
    return id ? parseInt(id, 10) : null;
    },
  },
};
</script>

<style>
#app {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
