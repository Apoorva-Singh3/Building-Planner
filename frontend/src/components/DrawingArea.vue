<template>
    <div class="drawing-area" @mousedown="startAction" @mousemove="performAction" @mouseup="stopAction">
        <DrawingShape v-for="shape in shapes" :key="shape.id" :shape="shape"
            :isSelected="selectedShape && selectedShape.id === shape.id" @select="selectShape" @resize="resizeShape" />
        <div v-if="showAnnotations">
            <ShapeAnnotation v-for="annotation in annotations" :key="annotation.id" :annotation="annotation" />
        </div>
    </div>
</template>

<script>
import DrawingShape from './DrawingShape.vue';
import ShapeAnnotation from './ShapeAnnotation.vue';
import axios from 'axios';

export default {
    components: { DrawingShape, ShapeAnnotation },
    props: {
        selectedTool: {
            type: String,
            required: true,
        },
        selectedShapeType: {
            type: String,
            required: true,
        },
        drawingId: {
            type: Number,
            required: false,
        },
    },
    data() {
        return {
            showAnnotations: false,
            shapes: [],
            annotations: [],
            selectedShape: null,
            actionType: null,
            startCoords: null,
        };
    },
    methods: {
        /**
 * @param {MouseEvent} event - The mouse event
 */
        startAction(event) {
            console.log('mousedown:', event);
            if (this.selectedTool === 'draw') {
                this.startDrawing(event);
            } else if (this.selectedTool === 'select' && this.selectedShape) {
                this.startResizingOrMoving(event);
            }
        },

        /**
         * @param {MouseEvent} event - The mouse event
         */
        performAction(event) {
            console.log('mousemove:', event);
            if (this.actionType === 'drawing') {
                this.drawing(event);
            } else if (this.actionType === 'resizing') {
                this.resizing(event);
            } else if (this.actionType === 'moving') {
                this.moving(event);
            }
        },

        /**
         * @param {MouseEvent} event - The mouse event
         */
        stopAction(event) {
            console.log('mouseup:', event);
            if (this.actionType === 'drawing') {
                this.stopDrawing();
            } else if (this.actionType === 'resizing' || this.actionType === 'moving') {
                this.stopResizingOrMoving();
            }
            this.actionType = null;
            this.startCoords = null;
        },

        startDrawing(event) {
            console.log('Start Drawing:', event.offsetX, event.offsetY);
            this.actionType = 'drawing';
            const newShape = {
                type: this.selectedShapeType,
                coordinates: { x1: event.offsetX, y1: event.offsetY, x2: event.offsetX, y2: event.offsetY },
            };
            this.shapes.push(newShape);
            console.log('Shapes:', this.shapes);
        },
        drawing(event) {
            const currentShape = this.shapes[this.shapes.length - 1];
            console.log('Drawing:', event.offsetX, event.offsetY);
            if (currentShape) {
                currentShape.coordinates.x2 = event.offsetX;
                currentShape.coordinates.y2 = event.offsetY;
            }
            console.log('Updated Shape:', currentShape);
        },
        stopDrawing() {
            console.log('Stopping Drawing');
            axios.post('/api/shapes', { drawing_id: this.drawingId, type: this.selectedShapeType, coordinates: this.shapes[this.shapes.length - 1].coordinates })
                .then(response => {
                    this.shapes[this.shapes.length - 1].id = response.data.id;
                });
        },
        startResizingOrMoving(event) {
            const shape = this.selectedShape;
            const { x1, y1, x2, y2 } = shape.coordinates;
            this.startCoords = { x: event.offsetX, y: event.offsetY };

            if (this.isNearEdge(event.offsetX, event.offsetY, x2, y2)) {
                this.actionType = 'resizing';
            } else if (this.isInsideShape(event.offsetX, event.offsetY, x1, y1, x2, y2)) {
                this.actionType = 'moving';
            }
        },
        resizing(event) {
            this.selectedShape.coordinates.x2 = event.offsetX;
            this.selectedShape.coordinates.y2 = event.offsetY;
        },
        moving(event) {
            const dx = event.offsetX - this.startCoords.x;
            const dy = event.offsetY - this.startCoords.y;
            const { x1, y1, x2, y2 } = this.selectedShape.coordinates;

            this.selectedShape.coordinates.x1 = x1 + dx;
            this.selectedShape.coordinates.y1 = y1 + dy;
            this.selectedShape.coordinates.x2 = x2 + dx;
            this.selectedShape.coordinates.y2 = y2 + dy;

            this.startCoords = { x: event.offsetX, y: event.offsetY };
        },
        stopResizingOrMoving() {
            axios.put(`/api/shapes/${this.selectedShape.id}`, {
                type: this.selectedShape.type,
                coordinates: this.selectedShape.coordinates,
            });
        },
        selectShape(shape) {
            this.selectedShape = shape;
        },
        isNearEdge(x, y, edgeX, edgeY) {
            const threshold = 5;
            return Math.abs(x - edgeX) < threshold && Math.abs(y - edgeY) < threshold;
        },
        isInsideShape(x, y, x1, y1, x2, y2) {
            return x >= Math.min(x1, x2) && x <= Math.max(x1, x2) && y >= Math.min(y1, y2);
        },
        toggleAnnotations() {
            this.showAnnotations = !this.showAnnotations;
        },
    },
    created() {
        if (this.drawingId) {
            axios.get(`/api/drawings/${this.drawingId}`)
                .then(response => {
                    // Populate shapes and annotations only if data exists
                    this.shapes = response.data.shapes || [];
                    this.annotations = response.data.annotations || [];
                })
                .catch(error => {
                    if (error.response && error.response.status === 404) {
                        console.log(`Drawing with ID ${this.drawingId} not found.`);
                        this.shapes = [];
                        this.annotations = [];
                    } else {
                        console.error("Failed to fetch drawing:", error);
                    }
                });
        } else {
            // Handle the case where drawingId is not provided
            console.log("No drawing ID provided.");
            this.shapes = [];
            this.annotations = [];
        }
    }

};
</script>

<style scoped>
.drawing-area {
    position: relative;
    width: 100%;
    height: 100%;
    border: 1px solid #ddd;
    background-color: #fff;
    cursor: crosshair;
}
</style>
