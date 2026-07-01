export const SITE_NAME = "Career Brownie";
export const SITE_TAGLINE = "India's AI-Powered Career Intelligence Platform";
export const SITE_DESCRIPTION =
  "Career Brownie helps students, graduates, and professionals discover their ideal career path with AI-powered guidance, expert counselling, and university admissions support.";

export const FOUNDER_NAME = "Muskan Sahani";
export const CONTACT_EMAIL = "careerbrownie@gmail.com";
export const CONTACT_PHONE = "+91 8171557334";
export const WHATSAPP_NUMBER = "918171557334";
export const WHATSAPP_MESSAGE = "Hi! I'd like to know more about Career Brownie career guidance services.";

export const SOCIAL_LINKS = {
  instagram: "https://instagram.com/careerbrownie",
  linkedin: "https://linkedin.com/company/careerbrownie",
  twitter: "https://twitter.com/careerbrownie",
  youtube: "https://youtube.com/@careerbrownie",
  facebook: "https://facebook.com/careerbrownie",
};

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const NAV_LINKS = [
  { label: "Home", href: "/" },
  {
    label: "Services",
    href: "/services",
    children: [
      { label: "Career Counselling", href: "/services/career-counselling" },
      { label: "University Admissions", href: "/services/university-admissions" },
      { label: "Study Abroad", href: "/services/study-abroad" },
      { label: "Career Intelligence", href: "/services/career-intelligence" },
      { label: "AI Career Guidance", href: "/services/ai-career-guidance" },
    ],
  },
  { label: "About", href: "/about" },
  { label: "Blog", href: "/blog" },
  { label: "Contact", href: "/contact" },
];

export const STATS = [
  { value: "50,000+", label: "Students Guided" },
  { value: "95%", label: "Success Rate" },
  { value: "500+", label: "Universities" },
  { value: "200+", label: "Expert Counsellors" },
];

export const TESTIMONIALS = [
  {
    id: 1,
    name: "Priya Sharma",
    role: "Engineering Student, IIT Delhi",
    avatar: "/testimonials/priya.jpg",
    content:
      "Career Brownie's AI guidance helped me discover my passion for data science. The personalized roadmap was exactly what I needed to crack my dream internship at a top tech company.",
    rating: 5,
    course: "B.Tech Computer Science",
  },
  {
    id: 2,
    name: "Arjun Mehta",
    role: "MBA Graduate, IIM Bangalore",
    avatar: "/testimonials/arjun.jpg",
    content:
      "The counselling sessions were incredibly insightful. My counsellor understood my background deeply and helped me craft the perfect MBA application strategy.",
    rating: 5,
    course: "MBA Finance",
  },
  {
    id: 3,
    name: "Sneha Patel",
    role: "Class 12 Student, Mumbai",
    avatar: "/testimonials/sneha.jpg",
    content:
      "I was completely lost about what to study after 12th. Career Brownie's career assessment identified my strengths and opened up career paths I had never even considered!",
    rating: 5,
    course: "Pre-University",
  },
  {
    id: 4,
    name: "Rahul Verma",
    role: "Software Engineer, Bangalore",
    avatar: "/testimonials/rahul.jpg",
    content:
      "The skill gap analysis was a game-changer. It pinpointed exactly what I needed to learn to transition from a mid-level to senior role. Got promoted within 6 months!",
    rating: 5,
    course: "Career Transition",
  },
];

export const COUNSELLORS = [
  {
    id: 1,
    name: "Dr. Ananya Singh",
    title: "Senior Career Counsellor",
    specialization: "Engineering & Technology",
    experience: "12 Years",
    sessions: "2,400+",
    rating: 4.9,
    image: "/counsellors/ananya.jpg",
    tags: ["IIT/NIT Admissions", "Tech Careers", "STEM Guidance"],
  },
  {
    id: 2,
    name: "Prof. Vikram Nair",
    title: "University Admissions Expert",
    specialization: "MBA & Business",
    experience: "15 Years",
    sessions: "3,200+",
    rating: 4.8,
    image: "/counsellors/vikram.jpg",
    tags: ["IIM Admissions", "CAT Prep", "B-School Guidance"],
  },
  {
    id: 3,
    name: "Ms. Preethi Kumar",
    title: "Study Abroad Specialist",
    specialization: "International Education",
    experience: "8 Years",
    sessions: "1,800+",
    rating: 4.9,
    image: "/counsellors/preethi.jpg",
    tags: ["USA Admissions", "UK Visas", "Scholarships"],
  },
];

export const SERVICES_LIST = [
  {
    id: "career-counselling",
    icon: "🧭",
    title: "Career Counselling",
    description:
      "One-on-one expert sessions to help you discover the perfect career path aligned with your interests, strengths, and goals.",
    href: "/services/career-counselling",
    color: "from-indigo-500 to-purple-600",
    features: ["Psychometric Assessment", "Aptitude Testing", "1:1 Expert Sessions", "Career Roadmap"],
  },
  {
    id: "university-admissions",
    icon: "🎓",
    title: "University Admissions",
    description:
      "Comprehensive support for college admissions — from shortlisting universities to crafting compelling applications.",
    href: "/services/university-admissions",
    color: "from-violet-500 to-pink-600",
    features: ["College Shortlisting", "SOP Writing", "Application Review", "Interview Prep"],
  },
  {
    id: "study-abroad",
    icon: "✈️",
    title: "Study Abroad",
    description:
      "Navigate international education with expert guidance on admissions, visas, scholarships, and accommodation.",
    href: "/services/study-abroad",
    color: "from-blue-500 to-cyan-600",
    features: ["Country Selection", "Visa Support", "Scholarship Guidance", "Pre-Departure Prep"],
  },
  {
    id: "career-intelligence",
    icon: "📊",
    title: "Career Intelligence",
    description:
      "Data-driven insights into job market trends, in-demand skills, salary benchmarks, and growth trajectories.",
    href: "/services/career-intelligence",
    color: "from-emerald-500 to-teal-600",
    features: ["Job Market Analysis", "Skill Gap Report", "Salary Benchmarks", "Industry Trends"],
  },
  {
    id: "ai-career-guidance",
    icon: "🤖",
    title: "AI Career Guidance",
    description:
      "India's most advanced AI career assistant — get instant, personalized career advice powered by cutting-edge AI.",
    href: "/services/ai-career-guidance",
    color: "from-orange-500 to-red-600",
    features: ["AI Chat Counsellor", "Instant Recommendations", "24/7 Availability", "Personalized Plans"],
  },
];

export const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Take Career Assessment",
    description:
      "Complete our comprehensive psychometric and aptitude assessment to discover your unique strengths, interests, and career personality.",
    icon: "📝",
  },
  {
    step: "02",
    title: "Get AI Insights",
    description:
      "Our AI engine analyzes your profile and generates personalized career recommendations, skill gap reports, and growth pathways.",
    icon: "🤖",
  },
  {
    step: "03",
    title: "Consult an Expert",
    description:
      "Connect with a specialized counsellor who reviews your AI report and helps you craft a tailored career strategy.",
    icon: "🎯",
  },
  {
    step: "04",
    title: "Execute Your Plan",
    description:
      "Follow your personalized career roadmap with milestones, resources, and ongoing support from our counsellors.",
    icon: "🚀",
  },
];

export const FAQS = [
  {
    q: "Who is Career Brownie for?",
    a: "Career Brownie serves students from Class 9-12, college students, graduates, working professionals, and parents seeking guidance for their children.",
  },
  {
    q: "How is AI career guidance different from human counselling?",
    a: "Our AI provides instant, data-driven insights 24/7, while human counsellors offer empathy, nuanced understanding, and personalized strategic advice. We combine both for the best outcome.",
  },
  {
    q: "How do I book a counselling session?",
    a: "Simply click 'Book Consultation', fill in your details, and choose a time slot that works for you. A counsellor will confirm your booking within 2 hours.",
  },
  {
    q: "What is the cost of a counselling session?",
    a: "We offer a free 30-minute introductory session. Full counselling packages start from ₹999. See our Pricing section for detailed plans.",
  },
  {
    q: "Do you help with study abroad applications?",
    a: "Yes! We provide end-to-end support for international admissions including country selection, university shortlisting, SOP writing, visa guidance, and scholarship applications.",
  },
  {
    q: "Is my data secure?",
    a: "Absolutely. We use bank-grade encryption to protect your personal information and career data. We never share your data with third parties without consent.",
  },
];
