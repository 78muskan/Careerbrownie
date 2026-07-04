export interface ContactLead {
  id: number;
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  source: string;
  created_at: string;
  is_contacted: boolean;
  notes: string;
}

export interface ConsultationBooking {
  id: number;
  name: string;
  email: string;
  phone: string;
  grade: string;
  service: string;
  preferred_date: string;
  preferred_time: string;
  message: string;
  source: string;
  status: "pending" | "confirmed" | "completed" | "cancelled" | "no_show";
  created_at: string;
  admin_notes: string;
}

export interface NewsletterSubscriber {
  id: number;
  email: string;
  name: string;
  subscribed_at: string;
  is_active: boolean;
}

export interface AdminStats {
  total_leads: number;
  total_bookings: number;
  total_subscribers: number;
  new_leads_today: number;
  pending_bookings: number;
  leads_by_source: Record<string, number>;
  bookings_by_status: Record<string, number>;
}
