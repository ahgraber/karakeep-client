set quiet := true
set shell := ['bash', '-euo', 'pipefail', '-c']
set dotenv-load := true

mod docs 'docs/'

[private]
default:
  @just --list --unsorted
