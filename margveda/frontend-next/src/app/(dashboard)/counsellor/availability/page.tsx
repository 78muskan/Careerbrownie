"use client";
import { useEffect, useState } from "react";
import { Plus, Trash2, Loader2, Clock } from "lucide-react";
import api from "@/lib/api";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

interface Slot {
  id: string;
  weekday: number;
  weekday_name: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  is_active: boolean;
}

export default function AvailabilityPage() {
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ weekday: 0, start_time: "09:00", end_time: "10:00", duration_minutes: 60 });
  const [adding, setAdding] = useState(false);
  const [showForm, setShowForm] = useState(false);

  const load = () => {
    api.get("/portal/slots/")
      .then((r) => setSlots(r.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const addSlot = async () => {
    setAdding(true);
    try {
      await api.post("/portal/slots/", form);
      load();
      setShowForm(false);
    } catch {
      alert("Failed to add slot.");
    } finally {
      setAdding(false);
    }
  };

  const deleteSlot = async (id: string) => {
    await api.delete(`/portal/slots/${id}/`);
    setSlots((s) => s.filter((x) => x.id !== id));
  };

  const toggleActive = async (slot: Slot) => {
    const { data } = await api.patch(`/portal/slots/${slot.id}/`, { is_active: !slot.is_active });
    setSlots((s) => s.map((x) => x.id === slot.id ? data : x));
  };

  const byDay = DAYS.map((day, i) => ({
    day, slots: slots.filter((s) => s.weekday === i),
  }));

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-bold text-gray-900">Availability</h1>
          <p className="text-gray-500 text-sm mt-1">Set your weekly available time slots for student bookings.</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2 text-sm">
          <Plus className="w-4 h-4" />
          Add Slot
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-primary-100">
          <h3 className="font-semibold text-gray-900 mb-4">New Time Slot</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Day</label>
              <select value={form.weekday} onChange={(e) => setForm({ ...form, weekday: parseInt(e.target.value) })}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
                {DAYS.map((d, i) => <option key={d} value={i}>{d}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Duration (min)</label>
              <select value={form.duration_minutes} onChange={(e) => setForm({ ...form, duration_minutes: parseInt(e.target.value) })}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
                {[30, 45, 60, 90, 120].map((d) => <option key={d} value={d}>{d} min</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Start Time</label>
              <input type="time" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">End Time</label>
              <input type="time" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
            </div>
          </div>
          <button onClick={addSlot} disabled={adding} className="btn-primary flex items-center gap-2 disabled:opacity-60">
            {adding && <Loader2 className="w-4 h-4 animate-spin" />}
            {adding ? "Adding…" : "Add Slot"}
          </button>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>
      ) : (
        <div className="space-y-3">
          {byDay.filter((d) => d.slots.length > 0).map(({ day, slots: daySlots }) => (
            <div key={day} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-3">{day}</h3>
              <div className="space-y-2">
                {daySlots.map((slot) => (
                  <div key={slot.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                    <Clock className="w-4 h-4 text-gray-400 shrink-0" />
                    <span className="text-sm text-gray-700">
                      {slot.start_time} – {slot.end_time}
                      <span className="text-gray-400 ml-1.5">({slot.duration_minutes} min)</span>
                    </span>
                    <div className="ml-auto flex items-center gap-3">
                      <button onClick={() => toggleActive(slot)}
                        className={`text-xs px-2.5 py-1 rounded-full font-medium transition-colors ${
                          slot.is_active ? "bg-green-100 text-green-700 hover:bg-green-200" : "bg-gray-100 text-gray-500 hover:bg-gray-200"
                        }`}>
                        {slot.is_active ? "Active" : "Paused"}
                      </button>
                      <button onClick={() => deleteSlot(slot.id)} className="p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
          {slots.length === 0 && (
            <div className="text-center bg-white rounded-2xl p-12 border border-gray-100">
              <Clock className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-500">No time slots configured yet.</p>
              <button onClick={() => setShowForm(true)} className="mt-4 btn-primary">Add your first slot</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
