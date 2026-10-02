import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.dirname(fileURLToPath(import.meta.url))
const manifest = JSON.parse(readFileSync(path.join(root, 'MIGRATION_BLOB_MANIFEST.json'), 'utf8'))

function gitBlobSha1(bytes) {
  const header = Buffer.from(`blob ${bytes.length}\0`)
  return createHash('sha1').update(header).update(bytes).digest('hex')
}

if (manifest.source_file_count !== manifest.files.length) {
  throw new Error(`manifest count mismatch: declared ${manifest.source_file_count}, listed ${manifest.files.length}`)
}

const failures = []
for (const entry of manifest.files) {
  const bytes = readFileSync(path.join(root, entry.path))
  const actual = gitBlobSha1(bytes)
  if (actual !== entry.git_blob_sha1) {
    failures.push({ path: entry.path, expected: entry.git_blob_sha1, actual })
  }
}

if (failures.length) {
  console.error('MIGRATION_BLOB_VALIDATION_FAILED')
  console.error(JSON.stringify(failures, null, 2))
  process.exit(1)
}

console.log(`MIGRATION_BLOB_VALIDATION_OK files=${manifest.files.length} source=${manifest.source_repository}@${manifest.source_commit}`)
