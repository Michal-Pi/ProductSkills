# Schema Subset

The package validators intentionally use Python standard-library code, not a full JSON Schema implementation.

Supported schema keywords in the local validator are:

- `$ref` for local repo schema files
- `type`
- `required`
- `properties`
- `additionalProperties: false`
- `enum`
- `const`
- `minLength`
- `minItems`
- `items` with a single object schema
- `allOf`
- `oneOf`
- `if` / `then`

Do not rely on unsupported JSON Schema keywords such as `anyOf`, `not`, `else`, `$defs`, JSON Pointer fragments, `pattern`, `patternProperties`, `dependentRequired`, tuple-style `items`, or `uniqueItems` unless the validator is extended first.
