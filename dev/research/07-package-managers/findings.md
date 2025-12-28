# R07: Package Manager Publishing - Research Findings

**Research ID**: R07  
**Status**: In Progress  
**Last Updated**: 2025-12-28

---

## Homebrew

### Tap Structure

- Dedicated tap repo recommended: `peternicholls/homebrew-safedownload`
- Formula lives under `Formula/safedownload.rb`
- Brew installs from GitHub release URLs with SHA256 verification

### Formula Template

```ruby
class Safedownload < Formula
	desc "Reliable, resumable downloads with verification"
	homepage "https://github.com/peternicholls/SafeDownload"
	version "1.3.0"
	on_macos do
		if Hardware::CPU.arm?
			url "https://github.com/peternicholls/SafeDownload/releases/download/v1.3.0/safedownload-v1.3.0-darwin-arm64.tar.gz"
			sha256 "<SHA256_ARM64>"
		else
			url "https://github.com/peternicholls/SafeDownload/releases/download/v1.3.0/safedownload-v1.3.0-darwin-amd64.tar.gz"
			sha256 "<SHA256_AMD64>"
		end
	end

	def install
		bin.install "safedownload"
	end

	test do
		assert_match "SafeDownload", shell_output("#{bin}/safedownload --version")
	end
end
```

### Automation

- Use goreleaser `brews` to publish formula to the tap from CI
- goreleaser auto-updates SHA256 and pushes commits to tap repo
- Keep formula tests minimal (e.g., `--version`)

---

## Debian Packaging

### .deb Structure

- Standard `ar` archive containing `debian-binary`, `control.tar.*`, `data.tar.*`
- Control fields include `Package`, `Version`, `Architecture`, `Depends`, `Description`

### Building with nfpm

```yaml
nfpm:
	formats: [deb]
	dependencies:
		- ca-certificates
		- curl
	homepage: https://github.com/peternicholls/SafeDownload
	maintainer: Peter Nicholls <maintainers@safedownload.dev>
	description: Reliable, resumable downloads with verification
	license: MIT
	deb:
		signature:
			key_file: ${DEB_SIGNING_KEY}
			passphrase: ${DEB_SIGNING_PASSPHRASE}
```

### APT Repository

- Initial approach: distribute `.deb` via GitHub Releases; install with `dpkg -i`
- Future: host apt repo via `reprepro`/`aptly` or a hosted service (Cloudsmith/PackageCloud)
- Repo metadata `Release` must be signed; packages may be signed

---

## RPM Packaging

### .rpm Spec File

- nfpm abstracts `.spec` but key fields: `Name`, `Version`, `Release`, `Summary`, `License`, `URL`, `Requires`

### Building

```yaml
nfpm:
	formats: [rpm]
	rpm:
		signature:
			key_file: ${RPM_SIGNING_KEY}
			passphrase: ${RPM_SIGNING_PASSPHRASE}
```

### YUM/DNF Repository

- Initial approach: distribute `.rpm` via GitHub Releases; install with `rpm -Uvh`
- Future: host repo with `createrepo` and `gpg` signing; or use hosted service

---

## goreleaser Integration

### Configuration

```yaml
brews:
	- name: safedownload
		tap:
			owner: peternicholls
			name: homebrew-safedownload
		commit_author:
			name: CI
			email: ci@safedownload.dev
		homepage: https://github.com/peternicholls/SafeDownload
		description: Reliable, resumable downloads with verification
		test: |
			system "#{bin}/safedownload", "--version"

nfpm:
	packages:
		- id: safedownload-deb
			file_name_template: safedownload_{{ .Version }}_{{ .Arch }}
			format: deb
		- id: safedownload-rpm
			file_name_template: safedownload-{{ .Version }}.{{ .Arch }}
			format: rpm
```

---

## Package Signing

- Generate dedicated GPG key; store private key securely in CI
- Use nfpm signing for `.deb` and `.rpm`
- Sign repo metadata when hosting apt/yum repos
- Publish signed `SHA256SUMS` alongside releases for defense-in-depth

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Created document | - |
| 2025-12-28 | Initialized research, added templates and tooling plan | Agent |
