/**
 * Every editable string on the sponsors page. Change copy, the price or the
 * contact address here; the page component reads from this module only.
 */

export const SPONSOR_EMAIL = 'manabi.build@gmail.com';
export const SPONSOR_EMAIL_SUBJECT = 'MANABI sponsorship enquiry';
export const SPONSOR_PRICE = '₹799';
export const SPONSOR_PRICE_NOTE = 'Founding price';
export const SPONSOR_SLOTS = 5;

export const SPONSOR_EMAIL_BODY = `Hi MANABI team,

Company:
Website:
One-line tagline (60 characters or fewer):
Contact name:
Duration (in months):

Thanks!`;

export const MAILTO_URL = `mailto:${SPONSOR_EMAIL}?subject=${encodeURIComponent(
  SPONSOR_EMAIL_SUBJECT,
)}&body=${encodeURIComponent(SPONSOR_EMAIL_BODY)}`;

/**
 * Desktop browsers with no default mail app silently ignore `mailto:` links,
 * so offer the same pre-filled message inside Gmail instead.
 */
export const GMAIL_COMPOSE_URL = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(
  SPONSOR_EMAIL,
)}&su=${encodeURIComponent(SPONSOR_EMAIL_SUBJECT)}&body=${encodeURIComponent(
  SPONSOR_EMAIL_BODY,
)}`;

export const HERO = {
  title: 'Partner with MANABI.',
  subline:
    'Put your product in front of students and developers who are actively choosing what to build.',
  cta: 'Become a sponsor',
  note: 'MANABI is early-stage. Founding sponsor price: ₹799/month.',
};

export const AUDIENCE = {
  index: '01',
  label: 'Audience',
  title: 'Who uses MANABI',
  intro:
    'MANABI helps students, developers and beginners pick real projects to build: for a resume, a hackathon or their first steps in code. Visitors browse project ideas by field and difficulty, build them, and prove their work with a verified GitHub repo.',
  cards: [
    {
      title: 'Students and resume builders',
      body: 'Looking for a real project for a resume, a portfolio or a final-year submission.',
    },
    {
      title: 'Hackathon participants',
      body: 'Hunting for something they can build inside a weekend and defend in front of judges.',
    },
    {
      title: 'Beginners and early-career developers',
      body: 'Starting out, with ideas sorted by difficulty so the next step is clear, and shipped work to show.',
    },
  ],
  statsLabel: 'Today on MANABI',
};

export const OFFER = {
  index: '02',
  label: 'The offer',
  title: 'One placement. Five slots.',
  intro:
    'A single placement: your logo, name and one-line tagline on the MANABI landing page, linked to your website. Pricing and period are agreed before we invoice.',
  cardTitle: 'Home-page sponsor',
  description:
    'Your logo, name and one-line tagline on the MANABI landing page, linked to your website.',
  bullets: [
    'Your logo, name and one-line tagline in the home-page sponsor strip',
    'A shoutout on our LinkedIn, X and Discord community',
    'Suggest your own project - it will be featured on the MANABI projects page',
    'Labelled “Sponsor”, never presented as a recommendation',
  ],
  cta: 'Email us about sponsorship',
  previewCaption: 'Preview of the home-page sponsor strip',
  previewFirstSlot: 'Your logo here',
  previewOtherSlot: 'Available',
  previewFirstName: 'Your product name',
  previewOtherName: 'Sponsor name',
};

export const PROMISE = {
  title: 'Our promise to students',
  text: 'Sponsorship never affects which projects are verified, how problems are ranked, or what we recommend. Sponsors are always labelled.',
};

export const HOW_IT_WORKS = {
  index: '03',
  label: 'How it works',
  title: 'From email to live in four steps',
  steps: [
    {
      title: 'Email us.',
      body: 'Tell us your company, website, tagline and how many months you want.',
    },
    {
      title: 'We confirm.',
      body: 'We confirm a free slot and send an invoice. We agree the payment method with you.',
    },
    {
      title: 'You approve.',
      body: 'We send a preview of your logo, name and link. Nothing goes live until you approve it.',
    },
    {
      title: 'Go live.',
      body: 'We publish within two working days of payment and your approval.',
    },
  ],
};

export const FAQ = {
  index: '04',
  label: 'FAQ',
  title: 'Questions sponsors ask',
  introPrefix: 'Anything else, email',
  items: [
    {
      id: 'duration',
      question: 'How long does a sponsorship last?',
      answer:
        'You pay ₹799 per month. Choose how many months you want - one, two, three or more. Nothing renews automatically, so when your period ends the placement is removed unless you book again.',
    },
    {
      id: 'preview',
      question: 'Can we see the placement first?',
      answer:
        'Yes. We send a preview of your logo, name and link before it goes live, and it only publishes once you approve it.',
    },
    {
      id: 'payment',
      question: 'How do we pay?',
      answer:
        'We send an invoice once the slot and period are agreed, and we agree the payment method with you. Your placement goes live within two working days of payment and your approval.',
    },
    {
      id: 'views',
      question: 'Do you guarantee views or clicks?',
      answer:
        'No. MANABI is early-stage and we do not guarantee views or clicks. Sponsors pay for a visible, labelled placement on the landing page, and any statistics we share are aggregate.',
    },
    {
      id: 'stop',
      question: 'What if we want to stop?',
      answer:
        'Your placement runs for the months you paid for and then ends. Tell us before your next month starts if you want to stop or change the duration. We remove the placement at the end of your paid period. If you cancel before your placement goes live, you get a full refund.',
    },
    {
      id: 'slots',
      question: 'What if all five slots are taken?',
      answer:
        'Slots are sold in the order they are confirmed. Email us and we will add you to the waiting list for the next opening.',
    },
    {
      id: 'changes',
      question: 'Can we change our logo or link during the placement?',
      answer: 'Yes, once per month at no cost. Email us the new files.',
    },
    {
      id: 'prohibited',
      question: 'What can’t you promote?',
      answer:
        'Anything misleading, illegal, adult, gambling or harmful.',
    },
    {
      id: 'data',
      question: 'Do you collect or share student data with sponsors?',
      answer:
        'No. Sponsors only see aggregate placement statistics. No individual student, account or repository data is shared, and we never sell data.',
    },
  ],
};
