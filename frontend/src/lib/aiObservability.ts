import { track } from '@/lib/analytics';

export interface ChatGeneration {
  sessionId: string;
  traceId: string;
  startedAt: number;
  outcome: 'success' | 'error';
  errorStatus?: number;
  turnCount: number;
  suggestionCount?: number;
}

/** Generates trace and conversation IDs accepted by AI Observability. */
export function createAiObservabilityId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  // `randomUUID` is only exposed in secure contexts, so keep a CSPRNG fallback
  // rather than a predictable Math.random() suffix.
  if (typeof crypto !== 'undefined' && typeof crypto.getRandomValues === 'function') {
    const bytes = crypto.getRandomValues(new Uint8Array(16));
    const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('');
    return `ai-${Date.now()}-${hex}`;
  }
  return `ai-${Date.now()}-${nextFallbackSequence()}`;
}

let fallbackSequence = 0;

function nextFallbackSequence(): number {
  return (fallbackSequence += 1);
}

/**
 * Records the existing backend-managed LLM call without delaying the chat UI.
 * Prompt and completion text is deliberately omitted: chat content stays
 * between the browser and the API. Only shape, latency and outcome are sent,
 * and the backend exposes no model/provider metadata to report either.
 */
export function captureChatGeneration({
  sessionId,
  traceId,
  startedAt,
  outcome,
  errorStatus,
  turnCount,
  suggestionCount,
}: ChatGeneration): void {
  track('$ai_generation', {
    $ai_trace_id: traceId,
    $ai_session_id: sessionId,
    $ai_span_name: 'catalog_chat',
    $ai_is_error: outcome === 'error',
    ...(errorStatus ? { $ai_http_status: errorStatus } : {}),
    ...(suggestionCount !== undefined
      ? { suggested_problem_count: suggestionCount }
      : {}),
    chat_turns: turnCount,
    $ai_latency: Math.max(0, (Date.now() - startedAt) / 1_000),
  });
}
