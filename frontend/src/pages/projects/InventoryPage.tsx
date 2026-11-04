import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/design/primitives';
import {
  listSalesChannels,
  createSalesChannel,
  SalesChannel,
  SalesChannelCreate,
  listInventoryItems,
  InventoryItem,
  InventoryItemCreate,
  createInventoryItem,
  listInventoryReservations,
  InventoryReservation,
  InventoryReservationCreate,
  createInventoryReservation,
  updateInventoryReservation,
  StockReconciliationCreate,
  createStockReconciliation,
  listStockReconciliations,
  StockReconciliation,
  getInventoryStats,
  InventoryStats,
} from '@/api/projects';

export function InventoryPage() {
  const [channels, setChannels] = useState<SalesChannel[]>([]);
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [reservations, setReservations] = useState<InventoryReservation[]>([]);
  const [reconciliations, setReconciliations] = useState<StockReconciliation[]>([]);
  const [stats, setStats] = useState<InventoryStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    const [ch, it, res, rec, st] = await Promise.all([
      listSalesChannels(),
      listInventoryItems(),
      listInventoryReservations(),
      listStockReconciliations(),
      getInventoryStats(),
    ]);
    setChannels(ch);
    setItems(it);
    setReservations(res);
    setReconciliations(rec);
    setStats(st);
    setLoading(false);
  }

  async function handleCreateChannel(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: SalesChannelCreate = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      channel_type: (form.elements.namedItem('channel_type') as HTMLInputElement).value,
    };
    const created = await createSalesChannel(body);
    setChannels([created, ...channels]);
  }

  async function handleCreateItem(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: InventoryItemCreate = {
      channel_id: 1,
      sku: (form.elements.namedItem('sku') as HTMLInputElement).value,
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      total_quantity: Number((form.elements.namedItem('total_quantity') as HTMLInputElement).value) || 0,
      available_quantity: Number((form.elements.namedItem('available_quantity') as HTMLInputElement).value) || 0,
    };
    const created = await createInventoryItem(1, body);
    setItems([created, ...items]);
  }

  async function handleReserve(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: InventoryReservationCreate = {
      item_id: 1,
      channel_id: 1,
      quantity: Number((form.elements.namedItem('quantity') as HTMLInputElement).value) || 1,
      external_order_id: (form.elements.namedItem('external_order_id') as HTMLInputElement).value || undefined,
    };
    const created = await createInventoryReservation(body);
    setReservations([created, ...reservations]);
    load();
  }

  async function handleConsume(id: number) {
    await updateInventoryReservation(id, { status: 'consumed' });
    load();
  }

  async function handleRelease(id: number) {
    await updateInventoryReservation(id, { status: 'released' });
    load();
  }

  async function handleReconcile(e: React.FormEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const body: StockReconciliationCreate = {
      item_id: 1,
      expected_quantity: Number((form.elements.namedItem('expected_quantity') as HTMLInputElement).value) || 0,
      actual_quantity: Number((form.elements.namedItem('actual_quantity') as HTMLInputElement).value) || 0,
      reason: (form.elements.namedItem('reason') as HTMLInputElement).value || undefined,
    };
    const created = await createStockReconciliation(body);
    setReconciliations([created, ...reconciliations]);
    load();
  }

  if (loading) return <p className="text-sm">Loading…</p>;

  return (
    <main className="mx-auto w-[min(1200px,96vw)] flex-1 py-10">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h1 className="font-display text-3xl uppercase leading-none">Inventory Reservation</h1>
        <Link to="/projects" className="font-mono text-[10px] font-bold uppercase tracking-widest text-accent underline-offset-4 hover:underline">
          &larr; All projects
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-4">
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Items</p>
          <p className="font-display text-2xl">{stats?.total_items ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Channels</p>
          <p className="font-display text-2xl">{stats?.total_channels ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Active Reservations</p>
          <p className="font-display text-2xl">{stats?.active_reservations ?? 0}</p>
        </div>
        <div className="border border-ink bg-sheet p-4">
          <p className="font-mono text-[10px] font-bold uppercase tracking-widest text-ink/50">Low Stock</p>
          <p className="font-display text-2xl">{stats?.low_stock_items ?? 0}</p>
        </div>
      </div>

      <section aria-label="Add channel" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Add Sales Channel
        </h2>
        <form onSubmit={handleCreateChannel} className="grid grid-cols-1 gap-3 sm:grid-cols-3 max-w-xl">
          <input
            name="name"
            placeholder="Channel name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="channel_type"
            placeholder="web/marketplace/pos/api"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <Button type="submit">Add Channel</Button>
        </form>
      </section>

      <section aria-label="Inventory items" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Inventory Items
        </h2>
        <form
          onSubmit={handleCreateItem}
          className="grid grid-cols-1 gap-3 sm:grid-cols-5 max-w-xl mb-4"
        >
          <input
            name="sku"
            placeholder="SKU"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="name"
            placeholder="Product name"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="total_quantity"
            type="number"
            placeholder="Total qty"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <input
            name="available_quantity"
            type="number"
            placeholder="Available qty"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <Button type="submit">Add Item</Button>
        </form>
        <ul className="divide-y border border-ink bg-sheet">
          {items.map((i) => (
            <li key={i.id} className="p-3 font-mono text-xs">
              <span className="font-bold">{i.sku}</span> — {i.name} — available: {i.available_quantity}/{i.total_quantity}
              <span className="ml-2 font-bold text-[9px] border-[1px] border-ink px-1">{i.available_quantity <= i.reorder_threshold ? 'LOW' : 'OK'}</span>
            </li>
          ))}
          {items.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No items yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Reservations" className="mb-8">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Reservations
        </h2>
        <form
          onSubmit={handleReserve}
          className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl mb-4"
        >
          <input
            name="quantity"
            type="number"
            placeholder="Qty"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="external_order_id"
            placeholder="Order ID"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <Button type="submit">Reserve</Button>
        </form>
        <ul className="divide-y border border-ink bg-sheet">
          {reservations.map((r) => (
            <li key={r.id} className="p-3 font-mono text-xs">
              Item #{r.item_id} — qty {r.quantity} — {r.status}
              <div className="flex gap-1 mt-1">
                {r.status === 'active' ? (
                  <>
                    <Button onClick={() => handleConsume(r.id)}>Consume</Button>
                    <Button onClick={() => handleRelease(r.id)} variant="secondary">Release</Button>
                  </>
                ) : null}
              </div>
            </li>
          ))}
          {reservations.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No reservations yet</li>
          )}
        </ul>
      </section>

      <section aria-label="Reconciliations">
        <h2 className="font-display text-xl uppercase md:text-2xl mb-4">
          Stock Reconciliation
        </h2>
        <form
          onSubmit={handleReconcile}
          className="grid grid-cols-1 gap-3 sm:grid-cols-4 max-w-xl"
        >
          <input
            name="expected_quantity"
            type="number"
            placeholder="Expected"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="actual_quantity"
            type="number"
            placeholder="Actual"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
            required
          />
          <input
            name="reason"
            placeholder="Reason"
            className="border border-ink bg-sheet p-2 font-mono text-sm"
          />
          <Button type="submit">Reconcile</Button>
        </form>
        <ul className="mt-4 divide-y border border-ink bg-sheet">
          {reconciliations.map((r) => (
            <li key={r.id} className="p-3 font-mono text-xs">
              Item #{r.item_id} — expected: {r.expected_quantity}, actual: {r.actual_quantity}, discrepancy: {r.discrepancy}
            </li>
          ))}
          {reconciliations.length === 0 && (
            <li className="p-3 font-mono text-xs text-center text-ink/50">No reconciliations yet</li>
          )}
        </ul>
      </section>
    </main>
  );
}
