# Token Limits

The `bundle-files` CLI now chunk bundles by an approximate context length so that no single artifact is overwhelmingly large for an LLM.
By default the tool starts a new part whenever the estimated token usage for the current bundle would exceed about 400,000 tokens.

## How chunking works

- The command estimates tokens for the header metadata and each file block as it streams them into the bundle.
- When adding the next block would push the total above the configured `--context-length`, the current output file is finalized and the next block begins a new part.
- Additional parts reuse the base output name, inserting `.partN` before the extension. For example, `bundle.md` would produce `bundle.md`, `bundle.part2.md`, and so on.
- If a single file is larger than the configured limit, it is still emitted on its own part and the CLI prints a warning so you can revisit the selection or raise the limit.

## Configuring the context length

Use the `--context-length` option to control the approximate token budget per part:

```bash
# Lower the target to 200k tokens per part
bundle-files --context-length 200000

# Disable token-based chunking entirely
bundle-files --context-length 0
```

Because the token count is an estimate, keep some headroom below the actual model context that you intend to use.

## Token estimation details

The estimator is intentionally lightweight and does not require third-party tokenizers. It assumes roughly four characters per token.
That heuristic keeps the CLI dependency-free and fast, but it also means the reported token totals are approximate.
When you need an exact count for a specific model, run the generated bundle through the tokenizer provided by that model before uploading it.
