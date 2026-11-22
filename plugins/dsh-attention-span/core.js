const FILLER_PATTERNS = [
  /^\s*(?:it should be noted that|it is important to note that|as a matter of fact|in order to|due to the fact that)\s+/i,
  /^\s*(?:следует отметить, что|важно отметить, что|необходимо отметить, что|для того, чтобы)\s+/i
]

const META_PATTERNS = [
  /\b(?:as mentioned above|as stated above|как было сказано выше|как уже отмечалось)\b[,:]?\s*/gi
]

function protectOpaque(text) {
  const protectedParts = []
  const value = text.replace(/\`\`\`[\\s\\S]*?\`\`\`|https?:\\/\\/\\S+/g, function (match) {
    const id = protectedParts.length
    protectedParts.push(match)
    return '__AS_OPAQUE_' + id + '__'
  })
  return { value, protectedParts }
}

function restoreOpaque(text, protectedParts) {
  return text.replace(/__AS_OPAQUE_(\\d+)__/g, function (_, index) {
    return protectedParts[Number(index)] ?? ''
  })
}

function normalizeWhitespace(text) {
  return text
    .replace(/[ \\t]+/g, ' ')
    .replace(/ *\\n *\\n */g, '\\n\\n')
    .replace(/ *\\n */g, '\\n')
    .trim()
}

function sentenceKey(sentence) {
  return sentence
    .toLocaleLowerCase()
    .replace(/[«»“”"'\`.,!?;:()[\\]{}—–-]/g, ' ')
    .replace(/\\s+/g, ' ')
    .trim()
}

function removeAdjacentDuplicateSentences(text) {
  const sentences = text.split(/(?<=[.!?])\\s+(?=[A-ZА-ЯЁ0-9«“])/u)
  const result = []
  let previous = null
  for (const sentence of sentences) {
    const key = sentenceKey(sentence)
    if (key && key === previous) continue
    result.push(sentence)
    previous = key || previous
  }
  return result.join(' ')
}

function removeFillerPrefixes(text) {
  let result = text
  for (const pattern of FILLER_PATTERNS) result = result.replace(pattern, '')
  for (const pattern of META_PATTERNS) result = result.replace(pattern, '')
  return result
}

function collapsePunctuation(text) {
  return text
    .replace(/!{2,}/g, '!')
    .replace(/\?{2,}/g, '?')
    .replace(/,{2,}/g, ',')
}

export function estimateTokens(text) {
  const normalized = text.trim()
  if (!normalized) return 0
  return Math.ceil(normalized.length / 4)
}

export function optimize(text, options = {}) {
  if (typeof text !== 'string') throw new TypeError('text must be a string')

  const maxReductionRatio = Number.isFinite(options.maxReductionRatio)
    ? Math.min(Math.max(options.maxReductionRatio, 0), 0.8)
    : 0.35

  const original = text
  const protectedInput = protectOpaque(original)

  let candidate = normalizeWhitespace(protectedInput.value)
  candidate = removeFillerPrefixes(candidate)
  candidate = candidate.replace(/(?:^|\n)\s*[-*]\s+/g, '$1')
  candidate = removeAdjacentDuplicateSentences(candidate)
  candidate = collapsePunctuation(candidate)
  candidate = normalizeWhitespace(candidate)
  candidate = restoreOpaque(candidate, protectedInput.protectedParts)

  const originalTokens = estimateTokens(original)
  const candidateTokens = estimateTokens(candidate)
  const reduction = originalTokens === 0
    ? 0
    : Math.max(0, (originalTokens - candidateTokens) / originalTokens)

  const accepted = reduction <= maxReductionRatio
  const optimized = accepted ? candidate : original
  const optimizedTokens = estimateTokens(optimized)

  return {
    original,
    optimized,
    changed: optimized !== original,
    accepted,
    reason: accepted ? 'conservative-optimization' : 'reduction-cap-exceeded',
    estimatedTokens: {
      before: originalTokens,
      after: optimizedTokens,
      saved: Math.max(0, originalTokens - optimizedTokens),
      reductionRatio: accepted ? reduction : 0
    },
    principles: {
      simplicity: true,
      brevity: accepted && optimized !== original,
      clarity: true,
      humanity: true
    }
  }
}
