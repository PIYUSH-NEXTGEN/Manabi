import { setupServer } from 'msw/node';
import { handlers, resetMockHandlersState } from './handlers';

export const server = setupServer(...handlers);
export { resetMockHandlersState };
