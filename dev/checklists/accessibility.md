# Accessibility Testing Checklist

**Constitution**: v1.5.0 - Principle XI (Accessibility)  
**Purpose**: Ensure TUI is accessible to all users regardless of visual abilities or terminal capabilities  
**Required For**: All TUI changes, theme updates, new visual indicators

## Visual Accessibility

### High-Contrast Mode
- [ ] TUI readable with `--theme high-contrast` flag
- [ ] Text has sufficient contrast ratio (WCAG AA: 4.5:1 minimum)
- [ ] Background colors don't interfere with text readability
- [ ] Status indicators visible without color (use shapes/symbols)
- [ ] Tested in both light and dark terminal backgrounds

### Color Blindness Support
- [ ] Status indicators don't rely solely on color
- [ ] Red/green combinations avoided or supplemented with symbols
- [ ] Each status has unique emoji + text label
- [ ] Tested with grayscale mode (convert screenshot to grayscale)
- [ ] Color palette verified with colorblind simulator tool

### Status Indicators
- [ ] All status states have both emoji AND text label
  - Example: `✅ Completed` not just `✅`
- [ ] Emoji followed by space and descriptive text
- [ ] Consistent pattern across all status types:
  - Queued: `⏳ Queued`
  - Downloading: `⬇️ Downloading`
  - Completed: `✅ Completed`
  - Failed: `❌ Failed`
  - Paused: `⏸️ Paused`

## Terminal Compatibility

### Narrow Terminals (80 columns)
- [ ] TUI gracefully degrades to 80-column width
- [ ] No horizontal scrolling required
- [ ] Long filenames truncated with ellipsis (e.g., `very-long-fi...ame.zip`)
- [ ] Progress bars adjust to available width
- [ ] Help text wraps properly

### Wide Terminals (>120 columns)
- [ ] TUI takes advantage of extra space
- [ ] Full filenames displayed when space available
- [ ] Additional columns shown (speed, ETA) when width permits
- [ ] Layout remains readable (not too sparse)

### Terminal Dimension Detection
- [ ] TUI detects current terminal size
- [ ] Layout adjusts dynamically on resize (if supported)
- [ ] Minimum width enforced (e.g., 60 columns)
- [ ] Error message shown if terminal too narrow

## Screen Reader Compatibility

### Text Structure
- [ ] Status updates announced sequentially
- [ ] Progress percentages included in text output
- [ ] No reliance on cursor position or ANSI escape codes for critical info
- [ ] Plain text mode available (`--plain` flag or auto-detected)

### Testing with Screen Readers
**macOS VoiceOver**:
- [ ] Open Terminal.app
- [ ] Enable VoiceOver (Cmd+F5)
- [ ] Run `safedownload --help` and verify help text is readable
- [ ] Start a download and verify progress updates are announced
- [ ] Navigate TUI with arrow keys and verify status announcements

**Linux Orca** (Ubuntu/Debian):
- [ ] Enable Orca screen reader
- [ ] Open terminal emulator
- [ ] Run SafeDownload and verify announcements
- [ ] Test slash commands and verify feedback

## Keyboard Navigation

### TUI Navigation
- [ ] All TUI functions accessible via keyboard
- [ ] No mouse required for any operation
- [ ] Arrow keys navigate queue items
- [ ] Tab key moves between UI sections (if multi-pane)
- [ ] Slash commands clearly documented
- [ ] `/help` command shows all keyboard shortcuts

### Slash Commands
- [ ] `/help` - Show help (always accessible)
- [ ] `/quit` or `/exit` - Exit TUI
- [ ] `/pause <id>` - Pause download
- [ ] `/resume <id>` - Resume download
- [ ] `/cancel <id>` - Cancel download
- [ ] `/purge` - Clear all state
- [ ] Commands case-insensitive

## Font and Rendering

### Unicode Support
- [ ] Emoji render correctly (or fallback to ASCII)
- [ ] No broken characters or replacement boxes (�)
- [ ] Tested with common terminal fonts (Monaco, Menlo, DejaVu Sans Mono)
- [ ] ASCII fallback mode available for legacy terminals

### Progress Bars
- [ ] Progress bars use ASCII characters (=, -, >, space)
- [ ] No reliance on Unicode block elements (█ ░ ▒ ▓)
- [ ] Percentage text included alongside visual bar
- [ ] Example: `[=========>          ] 45%`

## Testing Workflow

### Automated Tests
1. Run theme tests:
   ```bash
   go test ./pkg/ui/ -run TestHighContrastTheme
   go test ./pkg/ui/ -run TestColorblindSafeIndicators
   ```

2. Run terminal dimension tests:
   ```bash
   go test ./pkg/ui/ -run TestNarrowTerminal
   go test ./pkg/ui/ -run TestWideTerminal
   ```

### Manual Tests

#### Test 1: High-Contrast Visual Check
1. Set terminal to light background (white/light gray)
2. Run: `safedownload --theme high-contrast`
3. Verify text is readable with high contrast
4. Take screenshot for documentation

#### Test 2: Grayscale Test (Color Blindness)
1. Run TUI with normal theme
2. Take screenshot
3. Convert to grayscale using image editor
4. Verify all status indicators distinguishable without color
5. If any indicators look identical, add more visual differentiation

#### Test 3: Narrow Terminal (80 columns)
1. Resize terminal to exactly 80 columns:
   ```bash
   printf '\e[8;24;80t'  # 24 rows, 80 columns
   ```
2. Run SafeDownload with active downloads
3. Verify layout doesn't break or require horizontal scrolling
4. Verify filename truncation works correctly

#### Test 4: Screen Reader (macOS)
1. Enable VoiceOver: System Preferences → Accessibility → VoiceOver
2. Or use keyboard: Cmd+F5
3. Open Terminal.app
4. Run: `safedownload --help`
5. Verify VoiceOver reads help text correctly
6. Add a download and verify status updates are announced

#### Test 5: Screen Reader (Linux)
1. Install Orca: `sudo apt install orca`
2. Enable: `orca --replace &`
3. Open terminal
4. Run SafeDownload
5. Verify status announcements
6. Test slash commands

#### Test 6: Keyboard-Only Navigation
1. Disconnect mouse (or ignore it)
2. Run TUI
3. Navigate using only keyboard:
   - Arrow keys to move between items
   - Enter to select (if applicable)
   - Slash commands to control downloads
4. Verify all functions accessible

## Common Issues and Fixes

### Issue: Emoji not rendering
**Fix**: Add `--plain` flag to use ASCII fallback
```bash
safedownload --plain
```

### Issue: Status colors too similar
**Fix**: Use high-contrast theme
```bash
safedownload --theme high-contrast
```

### Issue: Text wrapping broken in narrow terminal
**Fix**: Implement dynamic width detection and text truncation
```go
// pkg/ui/layout.go
func truncateFilename(filename string, maxWidth int) string {
    if len(filename) <= maxWidth {
        return filename
    }
    // Keep extension visible
    ext := filepath.Ext(filename)
    baseLen := maxWidth - len(ext) - 3 // Reserve space for "..."
    return filename[:baseLen] + "..." + ext
}
```

### Issue: Screen reader announces ANSI codes
**Fix**: Detect screen reader mode and disable ANSI colors
```go
// Check for screen reader env vars
if os.Getenv("SCREEN_READER") == "true" || os.Getenv("TERM") == "dumb" {
    ui.plainMode = true
}
```

## Success Criteria

**All checkboxes must be checked before merging TUI changes.**

If any item fails:
1. Document the failure in GitHub issue
2. Implement fix according to "Common Issues and Fixes" section
3. Re-test and update checklist
4. Only merge when all items pass

## Documentation Requirements

After passing all checks:
- [ ] Update README.md with accessibility features section
- [ ] Document `--theme` flag options
- [ ] Document `--plain` flag for screen readers
- [ ] Add screenshots showing high-contrast mode
- [ ] Update CHANGELOG.md with accessibility improvements

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [macOS VoiceOver Guide](https://support.apple.com/guide/voiceover/welcome/mac)
- [Orca Screen Reader](https://help.gnome.org/users/orca/stable/)
- [Constitution Principle XI: Accessibility](../../.specify/memory/constitution.md)

---

**Last Updated**: 2025-12-25  
**Next Review**: Before each TUI-related release  
**Owner**: @peternicholls
