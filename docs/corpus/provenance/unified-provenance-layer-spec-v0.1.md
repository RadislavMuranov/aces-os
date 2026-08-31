# Unified Provenance Layer — Specification v0.1

Status: DRAFT for approval  
Date: 2026-08-13  
Depends on: DEEPSEEK-CORPUS-001 v1.0, CHATGPT-CORPUS-001 v1.0

## Purpose

Unified Provenance Layer (UPL) создаёт **общее адресное пространство происхождения**  
для двух независимых корпусов, не объединяя сами истории и не продвигая знания в Canon.

> UPL не объединяет истории.  
> Он объединяет только адресное пространство происхождения.

## Non-goals

- Слияние оригинальных архивов
- Автоматическая канонизация
- Удаление или понижение CONFIRMED источников
- Автоматическое разрешение конфликтов
- Принятие title-match как semantic equivalence

## Core Entities

### SourceConversation
- corpus_id: DEEPSEEK-CORPUS-001 | CHATGPT-CORPUS-001
- aces_id: DS-CHAT-XXXX | CG-CHAT-XXXX
- original_id: platform-native id
- stage0_status: CONFIRMED | REVIEW | EXCLUDED
- stage0_manifest_version: 1.0
- source_archive_hash: SHA-256
- conversation_hash: optional content hash
- date_start / date_end
- title
- source_location
- provenance_status: PRESERVED

### Rules
- CONFIRMED → eligible for P2
- REVIEW → retained; not confirmed knowledge
- EXCLUDED → negative provenance only; never knowledge source; never deleted from index

## Invariants

- Dual provenance forever
- Originals never merged
- Stage0 status is authoritative
- Canonical count starts at 0
- Cross-source relations are candidates only
- No silent promotion of EXCLUDED or REVIEW
- stage0_status cannot change without authorization event
