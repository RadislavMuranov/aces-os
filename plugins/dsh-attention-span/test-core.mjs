import assert from 'node:assert/strict'
import { estimateTokens, optimize } from './core.js'

const input = 'It should be noted that this is a test. This is a test. This is a test.'
const result = optimize(input)

assert.equal(result.changed, true)
assert.equal(result.accepted, true)
assert.match(result.optimized, /this is a test/i)
assert.ok(result.estimatedTokens.saved > 0)

const opaque = 'Keep this URL https://example.com/a?q=1 and this code: \`\`\`js
const x = 1
\`\`\`'
const protectedResult = optimize(opaque)
assert.match(protectedResult.optimized, /https:\\/\\/example\\.com\\/a\\?q=1/)
assert.match(protectedResult.optimized, /const x = 1/)

assert.equal(estimateTokens(''), 0)
console.log('attention-span core tests: PASS')
