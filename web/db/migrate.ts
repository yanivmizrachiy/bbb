import "dotenv/config";
import { migrateDb, closeDb, usingServer } from "./index";

if (!usingServer) {
  console.log("No Postgres server configured — nothing to migrate (snapshot mode).");
  process.exit(0);
}

migrateDb()
  .then(() => {
    console.log("migrated → server Postgres");
    return closeDb();
  })
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
