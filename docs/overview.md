# Overview

The client focuses on programmatic bookmark workflows for Karakeep:

- bookmark listing and pagination
- bookmark search
- bookmark create, update, and delete
- asset upload and retrieval
- tag and asset attach/detach operations

Primary package modules:

- `karakeep_client.karakeep`: async client, helpers, and runtime API calls
- `karakeep_client.models`: Pydantic models for Karakeep entities and responses
