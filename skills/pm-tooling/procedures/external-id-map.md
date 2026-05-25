# External ID Map

Use when keeping generated artifacts connected to external tools.

## Steps

1. Assign each local artifact a stable local ID.
2. Validate map shape against `../../../schemas/external-id-map.schema.json`.
3. Before creating an external item, check `.product-os/external-id-map.json`.
4. If a mapping exists, preview an update instead of a duplicate create.
5. If no mapping exists, preview a create operation.
6. After each confirmed write, record external IDs and source artifact references before issuing the next write.
7. Do not store API tokens, secrets, or credentials in `.product-os/external-id-map.json`.
8. For batch operations, checkpoint progress and show any partial failures.

## Output

Return local ID, external ID if known, proposed operation, and checkpoint notes.
