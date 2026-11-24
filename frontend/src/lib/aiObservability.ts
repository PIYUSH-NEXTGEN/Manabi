import type { ChatMessage, ChatOut } from '@/api/client';
import { isPostHogConfigured, posthog } from '@/lib/posthog';

export interface ChatGeneration {
  messages: ChatMessage[];
  sessionId: string;
  traceId: string;
  startedAt: number;
  reply?: ChatOut;
  errorStatus?: number;
}

/** Generates trace and conversation IDs accepted by AI Observability. */
export function createAiObservabilityId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `ai-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

/**
 * Records the existing backend-managed LLM call without delaying the chat UI.
 * The backend does not expose model or provider metadata, so those properties
 * are intentionally omitted instead of being guessed in the browser.
 */
export function captureChatGeneration({
  messages,
  sessionId,
  traceId,
  startedAt,
  reply,
  errorStatus,
}: ChatGeneration): void {
  if (!isPostHogConfigured) return;

  try {
    posthog.capture('$ai_generation', {
      $ai_trace_id: traceId,
      $ai_session_id: sessionId,
      $ai_span_name: 'catalog_chat',
      $ai_input: messages,
      ...(reply
        ? {
            $ai_output_choices: [
              { role: 'assistant', content: reply.reply },
            ],
          }
        : {
            $ai_is_error: true,
            ...(errorStatus ? { $ai_http_status: errorStatus } : {}),
          }),
      $ai_latency: Math.max(0, (Date.now() - startedAt) / 1_000),
    });
  } catch {
    // Analytics must never affect the chat request or its rendered response.
  }
}
