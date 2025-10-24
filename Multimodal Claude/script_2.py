
# Create a comprehensive workflow example showing how the system works end-to-end

workflow_example = """
# COMPLETE WORKFLOW EXAMPLE: Building a Game Inventory UI System
# Demonstrates Claude Multi-Agent Architecture for Full-Stack Development with Performance Optimization

## User Request:
"Build a high-performance game inventory system UI with drag-and-drop functionality, 
real-time updates, and optimized rendering for 1000+ items."

## ORCHESTRATOR AGENT (Claude Opus 4) - Execution Plan

### Phase 1: Requirements Analysis & Planning
The orchestrator receives the request and creates an execution plan:

1. **Task Decomposition:**
   - Architecture: Design overall system structure
   - Frontend: Implement inventory UI with drag-and-drop
   - Backend: Real-time data synchronization API
   - Performance: Optimize for 1000+ items rendering

2. **Dependencies Identified:**
   - Architecture must complete before implementation begins
   - Frontend and Backend can work in parallel after architecture
   - Performance optimization runs continuously and at end

3. **Agent Assignment:**
   - Architecture Agent: System design phase
   - Frontend Agent: UI implementation (parallel)
   - Backend Agent: API implementation (parallel)
   - Performance Agent: Continuous monitoring + final optimization

---

## ARCHITECTURE AGENT (Claude Sonnet 4) - System Design

### Input from Orchestrator:
- Functional requirements
- Performance constraints (1000+ items)
- Real-time update requirements

### Architecture Agent Output:

```json
{
  "system_architecture": {
    "component_hierarchy": {
      "InventoryContainer": {
        "responsibility": "Root container, state management",
        "children": ["InventoryGrid", "ItemDetailsPanel"]
      },
      "InventoryGrid": {
        "responsibility": "Virtual scrolling grid of items",
        "optimization": "Virtual scrolling for performance",
        "children": ["InventorySlot[]"]
      },
      "InventorySlot": {
        "responsibility": "Individual item container",
        "features": ["Drag source", "Drop target", "Item display"],
        "optimization": "React.memo with custom comparison"
      }
    },
    
    "state_machine": {
      "states": {
        "idle": "Default state, awaiting interaction",
        "dragging": "Item being dragged",
        "dropping": "Validating drop target",
        "updating": "Syncing with backend",
        "error": "Error state with retry option"
      },
      "transitions": {
        "idle -> dragging": "DRAG_START event",
        "dragging -> dropping": "DRAG_OVER_VALID_TARGET event",
        "dropping -> updating": "DROP_COMPLETE event",
        "updating -> idle": "SYNC_SUCCESS event",
        "updating -> error": "SYNC_FAILURE event",
        "error -> idle": "RETRY_SUCCESS event"
      }
    },
    
    "data_flow": {
      "state_management": "Zustand (lightweight, performant)",
      "real_time_sync": "WebSocket connection",
      "optimistic_updates": "Client-side immediate, server reconciliation",
      "conflict_resolution": "Last-write-wins with version tracking"
    },
    
    "performance_strategy": {
      "rendering": "Virtual scrolling (react-window)",
      "updates": "Batch state changes, RAF scheduling",
      "memory": "Object pooling for drag operations",
      "events": "Event delegation, throttled handlers"
    }
  }
}
```

---

## FRONTEND AGENT (Claude Sonnet 4) - UI Implementation

### Phase 1: Vision API Analysis (if mockup provided)

Using Claude Vision API to analyze design mockup:

```python
# Orchestrator calls Frontend Agent with design mockup
vision_analysis = await frontend_agent.analyze_design(mockup_image)

# Vision API extracts:
# - Grid layout: 8 columns, responsive
# - Item card structure: icon, name, quantity badge
# - Visual states: normal, hover, selected, dragging
# - Color scheme: dark theme, accent colors
# - Interactive elements: drag handles, quantity controls
```

### Phase 2: State Machine Implementation

Frontend Agent creates XState state machine:

```typescript
import { createMachine, assign } from 'xstate';

const inventoryStateMachine = createMachine({
  id: 'inventory',
  initial: 'idle',
  context: {
    items: [],
    draggedItem: null,
    targetSlot: null,
    pendingUpdates: []
  },
  states: {
    idle: {
      on: {
        DRAG_START: {
          target: 'dragging',
          actions: assign({
            draggedItem: (ctx, event) => event.item
          })
        },
        ITEMS_UPDATED: {
          actions: assign({
            items: (ctx, event) => event.items
          })
        }
      }
    },
    
    dragging: {
      on: {
        DRAG_OVER: {
          actions: assign({
            targetSlot: (ctx, event) => event.slot
          })
        },
        DROP: [
          {
            target: 'updating',
            cond: 'isValidDrop',
            actions: 'prepareUpdate'
          },
          {
            target: 'idle',
            actions: 'resetDrag'
          }
        ],
        DRAG_END: {
          target: 'idle',
          actions: 'resetDrag'
        }
      }
    },
    
    updating: {
      invoke: {
        src: 'syncWithBackend',
        onDone: {
          target: 'idle',
          actions: 'applyUpdate'
        },
        onError: {
          target: 'error',
          actions: 'logError'
        }
      }
    },
    
    error: {
      on: {
        RETRY: 'updating',
        CANCEL: 'idle'
      }
    }
  }
}, {
  guards: {
    isValidDrop: (ctx) => {
      return ctx.targetSlot && ctx.targetSlot.canAccept(ctx.draggedItem);
    }
  },
  actions: {
    prepareUpdate: assign({
      pendingUpdates: (ctx) => [...ctx.pendingUpdates, {
        item: ctx.draggedItem,
        target: ctx.targetSlot,
        timestamp: Date.now()
      }]
    }),
    resetDrag: assign({
      draggedItem: null,
      targetSlot: null
    })
  }
});
```

### Phase 3: Component Implementation with Optimizations

```typescript
// InventoryGrid.tsx - Optimized with virtual scrolling
import { FixedSizeGrid } from 'react-window';
import { memo, useCallback } from 'react';

const InventoryGrid = memo(({ items, onItemMove }) => {
  const columnCount = 8;
  const rowCount = Math.ceil(items.length / columnCount);
  const cellWidth = 100;
  const cellHeight = 100;
  
  // Memoized cell renderer to prevent unnecessary re-renders
  const Cell = useCallback(({ columnIndex, rowIndex, style }) => {
    const index = rowIndex * columnCount + columnIndex;
    const item = items[index];
    
    if (!item) return null;
    
    return (
      <div style={style}>
        <InventorySlot item={item} onMove={onItemMove} />
      </div>
    );
  }, [items, onItemMove, columnCount]);
  
  return (
    <FixedSizeGrid
      columnCount={columnCount}
      columnWidth={cellWidth}
      height={600}
      rowCount={rowCount}
      rowHeight={cellHeight}
      width={800}
    >
      {Cell}
    </FixedSizeGrid>
  );
});

// InventorySlot.tsx - Optimized individual slot
const InventorySlot = memo(({ item, onMove }) => {
  const [state, send] = useActor(inventoryService);
  
  const handleDragStart = useCallback((e) => {
    send({ type: 'DRAG_START', item });
    
    // GPU-accelerated drag preview
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setDragImage(
      createDragPreview(item), 
      0, 
      0
    );
  }, [item, send]);
  
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    send({ type: 'DROP', targetSlot: item.slot });
  }, [item, send]);
  
  return (
    <div
      className="inventory-slot"
      draggable
      onDragStart={handleDragStart}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      style={{
        // GPU acceleration
        transform: 'translateZ(0)',
        willChange: state.matches('dragging') ? 'transform' : 'auto'
      }}
    >
      <ItemIcon src={item.icon} />
      <ItemName>{item.name}</ItemName>
      {item.quantity > 1 && <QuantityBadge>{item.quantity}</QuantityBadge>}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison for optimization
  return (
    prevProps.item.id === nextProps.item.id &&
    prevProps.item.quantity === nextProps.item.quantity
  );
});
```

---

## BACKEND AGENT (Claude Sonnet 4) - API Implementation

### Backend Agent Output:

```typescript
// Real-time WebSocket server with optimistic updates
import { WebSocketServer } from 'ws';
import { createServer } from 'http';

class InventoryServer {
  private wss: WebSocketServer;
  private inventoryStore: Map<string, InventoryState>;
  
  constructor() {
    this.inventoryStore = new Map();
    this.setupWebSocketServer();
  }
  
  setupWebSocketServer() {
    this.wss = new WebSocketServer({ port: 8080 });
    
    this.wss.on('connection', (ws, req) => {
      const userId = this.authenticateUser(req);
      const userInventory = this.loadInventory(userId);
      
      // Send initial state
      ws.send(JSON.stringify({
        type: 'INITIAL_STATE',
        inventory: userInventory
      }));
      
      // Handle inventory updates
      ws.on('message', async (data) => {
        const message = JSON.parse(data.toString());
        
        if (message.type === 'MOVE_ITEM') {
          const result = await this.handleItemMove(
            userId,
            message.payload
          );
          
          // Broadcast to all connected clients
          this.broadcastUpdate(userId, result);
        }
      });
    });
  }
  
  async handleItemMove(userId, payload) {
    const { itemId, fromSlot, toSlot, timestamp } = payload;
    
    // Validate move
    const validation = await this.validateMove(userId, payload);
    if (!validation.valid) {
      return { success: false, error: validation.error };
    }
    
    // Apply update atomically
    const updated = await this.db.transaction(async (tx) => {
      await tx.updateItemSlot(itemId, toSlot);
      return await tx.getInventory(userId);
    });
    
    // Update cache
    this.inventoryStore.set(userId, updated);
    
    return { success: true, inventory: updated };
  }
  
  broadcastUpdate(userId, update) {
    this.wss.clients.forEach((client) => {
      if (client.userId === userId && client.readyState === 1) {
        client.send(JSON.stringify({
          type: 'INVENTORY_UPDATE',
          payload: update
        }));
      }
    });
  }
}

// RESTful API for batch operations
const apiRouter = express.Router();

apiRouter.get('/inventory/:userId', async (req, res) => {
  const inventory = await inventoryService.getInventory(req.params.userId);
  res.json(inventory);
});

apiRouter.post('/inventory/:userId/batch-move', async (req, res) => {
  const { moves } = req.body;
  const results = await inventoryService.batchMoveItems(
    req.params.userId,
    moves
  );
  res.json(results);
});
```

---

## PERFORMANCE AGENT (Claude Sonnet 4) - Optimization

### Phase 1: Continuous Monitoring

Performance Agent monitors during development:

```javascript
class PerformanceMonitor {
  constructor() {
    this.metrics = {
      fps: [],
      renderTimes: [],
      memoryUsage: [],
      eventLatency: []
    };
  }
  
  startMonitoring() {
    // FPS monitoring
    let lastFrame = performance.now();
    const measureFPS = () => {
      const now = performance.now();
      const fps = 1000 / (now - lastFrame);
      this.metrics.fps.push(fps);
      lastFrame = now;
      requestAnimationFrame(measureFPS);
    };
    measureFPS();
    
    // Memory monitoring
    setInterval(() => {
      if (performance.memory) {
        this.metrics.memoryUsage.push({
          used: performance.memory.usedJSHeapSize,
          total: performance.memory.totalJSHeapSize,
          timestamp: Date.now()
        });
      }
    }, 1000);
    
    // React DevTools Profiler integration
    if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
      this.setupReactProfiling();
    }
  }
  
  getBottlenecks() {
    return {
      lowFPS: this.metrics.fps.filter(fps => fps < 60),
      slowRenders: this.metrics.renderTimes.filter(t => t > 16),
      memoryLeaks: this.detectMemoryLeaks(),
      expensiveComponents: this.identifyExpensiveComponents()
    };
  }
}
```

### Phase 2: Applied Optimizations

Performance Agent identifies and applies optimizations:

```typescript
// Optimization 1: Object Pooling for Drag Operations
class DragOperationPool {
  private pool: DragOperation[] = [];
  private active = new Set<DragOperation>();
  
  constructor(initialSize = 20) {
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(this.createOperation());
    }
  }
  
  acquire(): DragOperation {
    let op = this.pool.pop();
    if (!op) {
      op = this.createOperation();
    }
    this.active.add(op);
    return op;
  }
  
  release(op: DragOperation) {
    this.resetOperation(op);
    this.active.delete(op);
    this.pool.push(op);
  }
  
  private createOperation(): DragOperation {
    return {
      itemId: null,
      sourceX: 0,
      sourceY: 0,
      offsetX: 0,
      offsetY: 0,
      preview: null
    };
  }
  
  private resetOperation(op: DragOperation) {
    op.itemId = null;
    op.sourceX = op.sourceY = 0;
    op.offsetX = op.offsetY = 0;
    op.preview = null;
  }
}

// Optimization 2: Batch Updates with RAF Scheduling
class UpdateScheduler {
  private pendingUpdates: Array<() => void> = [];
  private rafId: number | null = null;
  
  schedule(update: () => void) {
    this.pendingUpdates.push(update);
    
    if (!this.rafId) {
      this.rafId = requestAnimationFrame(() => {
        this.flush();
      });
    }
  }
  
  private flush() {
    const updates = this.pendingUpdates.splice(0);
    
    // Batch DOM reads
    const reads = updates.filter(u => u.type === 'read');
    reads.forEach(r => r());
    
    // Then batch DOM writes
    const writes = updates.filter(u => u.type === 'write');
    writes.forEach(w => w());
    
    this.rafId = null;
  }
}

// Optimization 3: Efficient Event Delegation
class EventDelegator {
  constructor(private container: HTMLElement) {
    this.setupDelegation();
  }
  
  private setupDelegation() {
    // Single listener for all slots
    this.container.addEventListener('dragstart', (e) => {
      const slot = (e.target as HTMLElement).closest('.inventory-slot');
      if (slot) {
        this.handleDragStart(slot, e);
      }
    });
    
    // Throttled drag over
    this.container.addEventListener('dragover', 
      this.throttle((e) => {
        const slot = (e.target as HTMLElement).closest('.inventory-slot');
        if (slot) {
          this.handleDragOver(slot, e);
        }
      }, 16) // ~60fps
    );
  }
  
  private throttle(fn: Function, ms: number) {
    let lastCall = 0;
    return (...args: any[]) => {
      const now = Date.now();
      if (now - lastCall >= ms) {
        lastCall = now;
        fn(...args);
      }
    };
  }
}
```

### Phase 3: Performance Validation

```javascript
// Performance benchmarks after optimization
const benchmarkResults = {
  before: {
    avgFPS: 45,
    renderTime: 22ms,
    memoryUsage: 180MB,
    dragLatency: 35ms
  },
  after: {
    avgFPS: 59,
    renderTime: 8ms,
    memoryUsage: 95MB,
    dragLatency: 12ms
  },
  improvements: {
    fps: '+31%',
    renderTime: '-64%',
    memory: '-47%',
    latency: '-66%'
  }
};
```

---

## ORCHESTRATOR - Final Synthesis

### Orchestrator aggregates all agent outputs:

```json
{
  "final_deliverable": {
    "architecture": {
      "component_hierarchy": "Defined",
      "state_machine": "XState implementation",
      "data_flow": "Zustand + WebSocket",
      "status": "✓ Complete"
    },
    
    "frontend": {
      "components": [
        "InventoryContainer",
        "InventoryGrid (virtualized)",
        "InventorySlot (memoized)"
      ],
      "state_management": "XState state machine",
      "optimizations_applied": [
        "Virtual scrolling",
        "Component memoization",
        "GPU acceleration",
        "Event delegation"
      ],
      "status": "✓ Complete"
    },
    
    "backend": {
      "api_type": "WebSocket + REST",
      "features": [
        "Real-time synchronization",
        "Optimistic updates",
        "Conflict resolution",
        "Batch operations"
      ],
      "status": "✓ Complete"
    },
    
    "performance": {
      "baseline": "60 FPS target",
      "achieved": "59 FPS average",
      "optimizations": [
        "Object pooling (-47% memory)",
        "RAF scheduling (-64% render time)",
        "Event delegation (-66% latency)"
      ],
      "status": "✓ Validated"
    },
    
    "integration_status": "✓ All agents synchronized",
    "ready_for_deployment": true
  }
}
```

---

## Key Patterns Demonstrated:

1. **Orchestrator-Worker Pattern**: Central coordination with parallel execution
2. **State Machine Architecture**: Predictable UI state management
3. **Performance-First Design**: Optimization integrated from architecture phase
4. **Multi-Agent Collaboration**: Specialized agents working in parallel
5. **Memory Management**: Object pooling and efficient data structures
6. **Event-Driven Communication**: Loose coupling between components
7. **Progressive Enhancement**: Continuous performance monitoring and optimization
"""

# Save workflow example
with open('workflow_example.md', 'w') as f:
    f.write(workflow_example)

print("Workflow example created successfully!")
print(f"\nDocument length: {len(workflow_example)} characters")
print("\nKey sections covered:")
sections = [
    "1. Orchestrator Execution Planning",
    "2. Architecture Agent System Design",
    "3. Frontend Agent UI Implementation",
    "4. Backend Agent API Development", 
    "5. Performance Agent Optimization",
    "6. Final Synthesis and Validation"
]
for section in sections:
    print(f"  {section}")
