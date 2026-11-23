/**
 * Public contact address, shared by the footer, the contact page and the
 * removal links.
 *
 * `VITE_CONTACT_EMAIL` is compiled into the bundle, so it is public
 * configuration rather than a secret. The fallback exists because the footer
 * and the removal links used to render nothing when the variable was unset,
 * which left the deployed site with no visible way to reach a human while the
 * contact page showed this same address.
 */
const FALLBACK_CONTACT_EMAIL = 'manabi.build@gmail.com';

export const CONTACT_EMAIL: string =
  import.meta.env.VITE_CONTACT_EMAIL || FALLBACK_CONTACT_EMAIL;
