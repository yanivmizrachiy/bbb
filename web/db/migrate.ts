import "dotenv/config";
import { migrateDb, closeDb, usingServer } from "./index";

migrateDb()
  .then(() => {
    console.log(`migrated → ${usingServer ? "server Postgres" : "PGlite"}`);
    return closeDb();
  })
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
