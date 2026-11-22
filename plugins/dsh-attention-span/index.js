import { defineTool } from '@deepseek-ai/dsh-tools'
import { optimize } from './core.js'

export const name = 'aces-attention-span'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'attention_span_optimize',
    description:
      'Conservatively optimize a draft for human attention using simplicity, brevity, clarity, and humanity. ' +
      'Returns the optimized text plus an approximate token-saving estimate. ' +
      'Does not call an external model and does not silently mutate session state.',
    parameters: {
      text: {
        type: 'string',
        required: true,
        description: 'Draft text to optimize.'
      },
      maxReductionRatio: {
        type: 'number',
        description: 'Maximum allowed estimated reduction ratio. Defaults to 0.35.'
      }
    },
    output: {
      schema: {
        type: 'object',
        properties: {
          optimized: { type: 'string' },
          changed: { type: 'boolean' },
          accepted: { type: 'boolean' },
          reason: { type: 'string' },
          estimatedTokens: { type: 'object' },
          principles: { type: 'object' }
        }
      },
      render: (_args, value) => [{
        type: 'text',
        text: JSON.stringify(value, null, 2)
      }]
    },
    async execute(args) {
      return optimize(args.text, {
        maxReductionRatio: args.maxReductionRatio
      })
    }
  }))
}
