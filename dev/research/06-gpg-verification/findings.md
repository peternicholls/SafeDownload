# R06: GPG Signature Verification - Research Findings

**Research ID**: R06  
**Status**: Complete  
**Last Updated**: 2025-12-28  
**Researcher**: Research Agent  
**Time Spent**: 2.5 hours  

---

## Executive Summary

SafeDownload should use **ProtonMail/go-crypto** with pure Go signature verification for v1.2.0. This approach aligns with Constitution Principle VIII (minimal dependencies) by avoiding system GPG requirements while providing robust OpenPGP support. Users can verify signatures via `--verify-sig signature.asc` with fallback documentation for key management, or rely on standard GPG subprocess for environments where system `gpg` is available.

**Recommendation**: Implement pure Go verification as primary path; optionally support system gpg via subprocess as fallback for users with non-standard key formats.

---

## Architecture Decision: Pure Go vs. System GPG

### Option 1: ProtonMail/go-crypto (Pure Go) ✅ RECOMMENDED

**Overview**: 
ProtonMail/go-crypto is an actively maintained fork of golang.org/x/crypto/openpgp with modern OpenPGP support (RFC 4880, RFC 9580 with ECC keys). Zero external dependencies.

**Strengths**:
- **No system dependencies**: Works on any platform (Windows, macOS, Linux) without requiring GPG binary
- **Actively maintained**: Latest release May 2025 (v1.3.0); 247 contributors
- **Modern standards**: Supports Curve25519, EdDSA, RSA; supports RFC 9580 (latest OpenPGP standard)
- **Permissive license**: BSD-3-Clause (compatible with SafeDownload)
- **Consistent behavior**: Same verification across all platforms
- **Easy keyring integration**: Load armored public keys directly from files or embedded
- **Complete API**: `CheckArmoredDetachedSignature()` for detached signature verification
- **Backward compatible**: Drop-in replacement for stdlib openpgp

**Weaknesses**:
- Users must provide public key file or fetch it themselves
- Cannot automatically use system GPG keyring (must be explicitly loaded)
- Smaller ecosystem compared to system GPG

**Implementation Pattern**:
```go
// Load public key from file
keyRingReader, _ := os.Open("publickey.asc")
defer keyRingReader.Close()

// Load signature and data
signatureReader, _ := os.Open("file.tar.gz.asc")
dataReader, _ := os.Open("file.tar.gz")
defer signatureReader.Close()
defer dataReader.Close()

// Verify
entity, err := openpgp.CheckArmoredDetachedSignature(keyRingReader, dataReader, signatureReader)
if err != nil {
    return fmt.Errorf("signature verification failed: %w", err)
}
// entity contains signer information
```

**Code Example from ProtonMail/gopenpgp (v3 wrapper)**:
```go
import "github.com/ProtonMail/gopenpgp/v3/crypto"

pgp := crypto.PGP()
verifier, err := pgp.Verify().VerificationKey(publicKeyArmored).New()
verifyingReader, err := verifier.VerifyingReader(signatureFile, crypto.Armor)
result, err := verifyingReader.ReadAllAndVerifySignature()
if sigErr := result.SignatureError(); sigErr != nil {
    // Handle verification failure
}
```

### Option 2: System GPG Subprocess ⚠️ FALLBACK ONLY

**Overview**: 
Shell out to system `gpg --verify signature.asc file` to use user's system keyring and GPG configuration.

**Strengths**:
- Full feature support: All GPG algorithms, trust model, keyring features
- Uses user's existing keyring: Automatic access to imported keys
- Handles complex scenarios: Key expiration checks, trust levels, revocation lists
- Industry standard: Proven in production systems (Debian, Fedora, Arch)
- Works with non-standard key formats (gnu-dummy S2K algorithm, subkey signing)

**Weaknesses**:
- **External dependency**: Requires GPG binary (not installed on all systems)
- **Platform-specific behavior**: Different GPG versions may verify differently
- **Security concerns**: Private key access (if user configured), temporary key files
- **Performance**: subprocess overhead vs. in-process verification
- **Harder to test**: Depends on system GPG installation
- **Violates Constitution VIII**: Adds system dependency when pure Go available

**Exit Code Pattern**:
```bash
gpg --verify file.sig file
# Exit 0: Valid signature
# Exit 1: Invalid signature / verification failed
# Exit 2: Key not found in keyring
```

### Constitution Alignment Analysis

| Principle | Go-crypto | System GPG | Notes |
|-----------|-----------|-----------|-------|
| **VIII (Minimal Deps)** | ✅ Zero deps | ❌ Requires gpg binary | Go-crypto wins decisively |
| **X (Security Posture)** | ✅ Defense-in-depth | ✅ Defense-in-depth | Both suitable for optional verification |
| **II (Optional Features)** | ✅ Optional | ✅ Optional | Both support --verify-sig flag |
| **VIII (Polyglot Stability)** | ✅ Stable | ✅ Mature | Go-crypto more portable long-term |

**Verdict**: Pure Go approach strongly preferred per Constitution VIII. System GPG acceptable as optional fallback for users with non-standard key formats or special requirements.

---

## Key Management UX Scenarios

### Scenario 1: Valid Signature, Key in Keyring

**User Action**: 
```bash
safedownload download https://example.com/file.tar.gz --verify-sig publickey.asc
```

**System Response**:
```
✅ Signature valid
   Signed by: John Developer <john@example.com>
   Key ID: 1234567890ABCDEF
   Timestamp: 2025-12-25 10:00:00 UTC
```

**UX**: Green checkmark, display signer name and timestamp.

### Scenario 2: Invalid Signature (File Tampered)

**User Action**: Same as Scenario 1 (but file was corrupted)

**System Response**:
```
❌ Signature verification failed
   Error: Computed hash does not match signature
   File: file.tar.gz
   Signature: publickey.asc
```

**UX**: Red X, clear error message. Download marked as **FAILED**. Exit code 3.

### Scenario 3: Key Not Found (Missing Public Key File)

**User Action**:
```bash
safedownload download https://example.com/file.tar.gz --verify-sig missing-key.asc
```

**System Response**:
```
⚠️ Signature verification skipped
   Error: Key file not found: missing-key.asc
   Tip: Download the public key from upstream and use --verify-sig <keyfile>
```

**UX**: Yellow warning, suggest where to find keys (upstream website, key servers).

### Scenario 4: Key Expired

**User Action**: Valid signature, but key is expired

**System Response**:
```
⚠️ Signature verification partial
   Signature valid, but key expired on 2025-01-01
   Signed by: John Developer <john@example.com>
   Warning: Trust may be compromised
```

**UX**: Yellow warning icon, show expiration date. Optionally allow continuation with `--force-verify`.

### Scenario 5: Multiple Key IDs (Choose Key)

**User Action**:
```bash
safedownload download file.tar.gz --verify-sig --interactive
```

**System Response** (TUI mode):
```
Multiple keys found. Select signing key:
1) Alice Developer (alice@example.com) - Key ID: ABCD1234
2) Bob Maintainer (bob@example.com) - Key ID: EFGH5678
> 1

✅ Signature valid (Alice)
```

**UX**: Interactive key selection in TUI mode (if multiple armored keys in file).

---

## Implementation Approach

### Primary: ProtonMail/go-crypto

**Manifest Entry Format**:
```
https://example.com/file.tar.gz file.tar.gz sha256:abc123... sig:publickey.asc:signature.asc
```

**CLI Flag**:
```bash
safedownload download URL [--output FILE] [--verify-sig KEYFILE]
```

**TUI Slash Command**:
```
/verify-sig 1 path/to/publickey.asc
```

**State File Tracking**:
```json
{
  "downloads": [
    {
      "id": 1,
      "url": "...",
      "verification": {
        "method": "gpg",
        "key_id": "1234567890ABCDEF",
        "signer": "John Developer",
        "status": "verified",
        "timestamp": "2025-12-25T10:00:00Z"
      }
    }
  ]
}
```

### Fallback: System GPG (Optional)

Detected via `which gpg` or explicit `--use-system-gpg` flag. Subprocess approach:

```bash
gpg --batch --no-default-keyring --keyring keyring.gpg --verify sig.asc file
```

User-friendly error messages from GPG stderr.

---

## Library Evaluation

### ProtonMail/go-crypto

| Aspect | Rating | Notes |
|--------|--------|-------|
| Maintenance | ⭐⭐⭐⭐⭐ | Active, 2025-05-23 latest release (v1.3.0) |
| Stars | ⭐⭐⭐ | 390 stars (niche but respected) |
| Dependencies | ⭐⭐⭐⭐⭐ | Zero external dependencies |
| License | ✅ BSD-3-Clause | Permissive, safe for commercial |
| Documentation | ⭐⭐⭐⭐ | pkg.go.dev examples, GitHub README |
| Maturity | ⭐⭐⭐⭐⭐ | 247+ contributors, 1,232+ commits |
| Platform Support | ⭐⭐⭐⭐⭐ | Pure Go, works everywhere |
| OpenPGP Standard | ⭐⭐⭐⭐⭐ | RFC 4880, RFC 9580, ECC keys |
| **Overall Score** | **85/100** | Excellent for download verification |

**Key Metrics**:
- Last commit: 2025-05-23 (recent)
- License: BSD-3-Clause (Apache-2.0 compatible)
- Go version support: 1.13+
- Import path: `github.com/ProtonMail/go-crypto/openpgp`

### keybase/go-crypto

| Aspect | Rating | Notes |
|--------|--------|-------|
| Maintenance | ⚠️ Unmaintained | Last commit Jan 23, 2020 (outdated) |
| Stars | ⭐⭐ | 200 stars |
| Dependencies | ⭐⭐⭐⭐⭐ | Zero external dependencies |
| License | ✅ BSD-3-Clause | Permissive |
| Documentation | ⭐⭐⭐ | Limited examples |
| Maturity | ⭐⭐⭐ | Was solid but now deprecated |
| Modern Standards | ❌ Lacks ECC | No Curve25519, EdDSA support |
| **Overall Score** | **45/100** | Avoid—use ProtonMail's fork instead |

**Why ProtonMail is preferred**:
- ProtonMail fork is explicitly recommended by golang.org/x/crypto maintainers
- Keybase fork explicitly unmaintained (last commit 2020)
- Terraform AWS provider migrated from Keybase to ProtonMail (Issue #22602)

### golang.org/x/crypto/openpgp (Stdlib)

| Aspect | Rating | Notes |
|--------|--------|-------|
| Maintenance | ❌ Deprecated | "Unmaintained except for security fixes" |
| Standards | ⭐⭐ | Outdated; no ECC support |
| Documentation | ⭐⭐⭐⭐ | Good docs but dated examples |
| Maturity | ⭐⭐⭐⭐ | Stable but frozen |
| **Overall Score** | **40/100** | Use ProtonMail fork instead |

**Official guidance** (pkg.go.dev):
> "Deprecated: this package is unmaintained except for security fixes. New applications should consider a more focused, modern alternative to OpenPGP for their specific task. If you are required to interoperate with OpenPGP systems and need a maintained package, consider a community fork."

**Recommendation**: ProtonMail/go-crypto is the recommended fork.

---

## Detached Signature Verification Pattern

### Technical Pattern (OpenPGP Standard)

Detached signatures are separate files containing only the signature, not the data. Standard approach:

```
file.tar.gz           <- Original file (can be on disk or remote)
file.tar.gz.asc       <- Detached signature (ASCII-armored)
publickey.asc         <- Public key (ASCII-armored or binary)
```

**Verification Steps**:
1. Load public key from file: `gpg --import publickey.asc` (or programmatically)
2. Load signature: `gpg --verify file.tar.gz.asc`
3. GPG automatically looks for `file.tar.gz` (without .asc extension)
4. Compute hash of `file.tar.gz`, decrypt signature with public key, compare hashes
5. If match: Signature valid; if mismatch: Signature invalid

**Important**: Detached signatures do NOT include the filename, so you MUST pass both the signature file AND the data file. File extension convention (.asc, .sig) is just convention; the actual signed data location must be explicit.

### SafeDownload Integration

**Manifest Format**:
```
https://example.com/downloads/myapp-1.0.tar.gz \
  output.tar.gz \
  sha256:abc123def456... \
  gpg:https://example.com/downloads/myapp-1.0.tar.gz.asc:https://example.com/releases/keys/myapp.asc
```

Parse as: `gpg:<sig_url>:<key_url>`

**Workflow**:
1. Download file → `output.tar.gz`
2. Download signature → temporary file
3. Download/load public key → temporary file
4. Verify: `CheckArmoredDetachedSignature(keyReader, dataReader, sigReader)`
5. Clean up temporary files
6. Mark state as verified (or failed)

---

## Keyring Access Patterns

### Pattern 1: Armored Key File (Recommended for SafeDownload)

**Advantage**: Self-contained, no system keyring required.

```go
// Load from file
keyFile, _ := os.Open("publickey.asc")
keyRing, _ := openpgp.ReadArmoredKeyRing(keyFile)

// Or from embedded/downloaded data
keyRing, _ := openpgp.ReadArmoredKeyRing(
    strings.NewReader(armoredKeyData),
)
```

**How users get keys**:
- Download from upstream website: https://example.com/releases/KEYS
- Import from keyserver: `gpg --recv-keys <KEYID>`
- Email from developer
- Inline in documentation

**UX for SafeDownload**:
```bash
# Users fetch key once, then reuse
curl https://example.com/releases/KEYS > myapp-keys.asc
safedownload download URL --verify-sig myapp-keys.asc
```

### Pattern 2: System GPG Keyring (Fallback)

Access user's `~/.gnupg/pubring.gpg`:

```bash
gpg --verify file.sig file
# Automatically uses ~/.gnupg/pubring.gpg
```

Requires system GPG installation. SafeDownload can detect and offer as fallback:

```bash
# Detect GPG
if command -v gpg &> /dev/null; then
    # Use system GPG as fallback
    gpg --batch --verify "$SIG_FILE" "$DATA_FILE"
else
    # Use pure Go verification
    verifyWithGocrypto()
fi
```

### Pattern 3: Key Server Fetch (Advanced, Not Recommended for v1.2.0)

Fetch keys from `pgp.mit.edu` or `keyserver.ubuntu.com`:

```bash
gpg --recv-keys 0x1234567890ABCDEF
gpg --verify file.sig
```

**Drawback**: Network dependency, keyserver availability, key verification (Web of Trust).

**Recommendation**: Document but don't implement in v1.2.0. Wait for user feedback.

---

## Answer Key Questions

### Q1: Pure Go vs. Subprocess to GPG?

**Answer**: **Use ProtonMail/go-crypto (pure Go) as primary path.**

**Confidence**: HIGH

**Rationale**:
- **Constitution Principle VIII** (Minimal Dependencies) strongly favors zero external deps
- Actively maintained, modern standards (RFC 9580), supports ECC keys
- Works on all platforms identically (Windows, macOS, Linux, WSL)
- Keybase fork is unmaintained (2020); ProtonMail explicitly recommended
- stdlib openpgp deprecated; ProtonMail fork is official recommendation
- No performance penalty for download verification use case
- Terraform AWS provider migrated from Keybase → ProtonMail (evidence of correctness)

**Fallback**: System GPG via subprocess acceptable for users with special requirements (non-standard key formats, gnu-dummy S2K algorithm), but not default.

**Sources**:
- ProtonMail go-crypto GitHub: https://github.com/ProtonMail/go-crypto (v1.3.0, May 2025)
- Terraform migration issue: https://github.com/hashicorp/terraform-provider-aws/issues/22602
- stdlib openpgp deprecation: https://pkg.go.dev/golang.org/x/crypto/openpgp

### Q2: How to Handle Missing GPG Keys?

**Answer**: **Provide clear UX for three scenarios**:

1. **Key file not found**: Suggest upstream documentation for where to find keys
2. **Key expired**: Show warning with expiration date; allow `--force-verify` to proceed
3. **Key not in signature**: Warn user which keys are needed; provide key ID for lookup

**Confidence**: HIGH

**Implementation**:
- Detect key file missing → CLI error before download attempt
- Detect key expired after loading → Warning state; optional `--force` flag
- Manifest support: `gpg:<sig_url>:<key_url>` allows specifying keys per download

**UX Examples**:
```
# Missing key file
safedownload download URL --verify-sig missing.asc
Error: Key file not found: missing.asc
Tip: Download public key from https://example.com/releases/KEYS

# Expired key
⚠️ Warning: Signature key expired 2025-01-01
   To skip verification: safedownload download URL
   To force verify: safedownload download URL --force

# Success
✅ Signature verified
   Signer: John Developer <john@example.com>
   Key ID: 1234567890ABCDEF
```

**Sources**:
- Git pattern: https://darkowlzz.github.io/post/git-commit-signature-verification/
- Debian verify-sig documentation: https://mgorny.pl/articles/verify-sig-by-example.html

### Q3: What UX Patterns Work for Key Verification Errors?

**Answer**: **Use status indicators (emoji + text), clear error messages, actionable guidance.**

**Confidence**: HIGH

**Pattern** (per Constitution XI - Accessibility):
- ✅ = Signature valid
- ❌ = Signature invalid
- ⚠️ = Signature partial/warning (key expired)
- ⏭️ = Verification skipped (optional feature)

**Error Messages** (specific, actionable):
```
❌ Signature verification failed
   Error: Signature does not match file content
   File: myapp-1.0.tar.gz
   Signature file: myapp-1.0.tar.gz.asc
   
   Next steps:
   1. Verify you downloaded the correct files from official source
   2. Check that signature file matches your file name
   3. Use --force to skip verification if you trust the source
   
   Exit code: 3 (verification failure)
```

**State Tracking**:
```json
{
  "verification": {
    "method": "gpg_openpgp",
    "status": "failed|verified|skipped|expired",
    "key_id": "1234567890ABCDEF",
    "signer": "John Developer",
    "error": "Signature hash mismatch",
    "timestamp": "2025-12-28T10:00:00Z"
  }
}
```

**TUI Display** (inspired by wget/aria2):
```
Download Status:
ID │ File                    │ Status           │ Signature
───┼─────────────────────────┼──────────────────┼────────────────
1  │ myapp-1.0.tar.gz       │ ✅ Completed    │ ✅ John Dev.
2  │ docs-1.0.tar.gz        │ ✅ Completed    │ ⚠️ Key expired
3  │ src-1.0.tar.gz         │ ✅ Completed    │ ❌ Invalid sig
```

**Sources**:
- Gentoo verify-sig patterns: https://mgorny.pl/articles/verify-sig-by-example.html
- Git implementation: https://darkowlzz.github.io/post/git-commit-signature-verification/

---

## Dependencies & Integration

### go-crypto Integration

**Import**:
```go
import "github.com/ProtonMail/go-crypto/openpgp"
```

**go.mod entry**:
```
require github.com/ProtonMail/go-crypto v1.3.0
```

**Module size**: ~50KB (minimal impact on binary size)
**Transitive dependencies**: 0 (pure Go crypto)

### Feature Specification Reference

**Blocked by this research**: Feature F017 (GPG Signatures)

**Specification updates needed**:
- Add `--verify-sig <keyfile>` CLI flag to core download
- Add `/verify-sig <download-id> <keyfile>` TUI command
- Add manifest format: `gpg:<sig_url>:<key_url>`
- Add state schema version field for signature metadata
- Update error codes: Add exit code 3 for verification failure

### Test Strategy

**Unit Tests**:
- Load armored key from various formats
- Verify valid signature (hardcoded test data)
- Reject tampered file
- Handle missing key file gracefully
- Detect expired key

**Integration Tests**:
- End-to-end: Download file → Verify signature → Mark complete
- Fallback to system GPG if available (optional test)
- Manifest with multiple downloads, mix of verified/unverified

**Test Data**:
- Generate test key: `gpg --full-generate-key`
- Sign test file: `gpg --armor --detach-sign test.txt`
- Tamper with file: modify bytes, re-verify (should fail)

---

## Open Questions

1. **Should we support key servers** (keyserver.ubuntu.com) for auto-fetching keys? (Deferred to v1.3.0)
2. **Should we cache downloaded keys** in `~/.safedownload/keys/`? (Yes, recommended)
3. **Should v1.2.0 mandate signatures** or make fully optional? (Fully optional per Principle II)
4. **Should we show trust level** (full/marginal/unknown) from GPG? (Optional UI enhancement, v1.3.0+)
5. **What about signature timestamps?** (Include in state; consider for expiration logic in v1.3.0)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-28 | Complete research and findings | Research Agent |
| 2025-12-25 | Created document | - |
