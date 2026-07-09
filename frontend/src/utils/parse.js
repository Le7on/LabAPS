// Small input parsing helpers shared by laboratory forms.

// "pcr, spin" -> ["pcr", "spin"]
export function parseList(value) {
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

// "0-40, 60-100" -> [[0, 40], [60, 100]]
export function parseWindows(value) {
  return parseList(value)
    .map((pair) => pair.split('-').map((n) => Number(n.trim())))
    .filter((w) => w.length === 2 && !Number.isNaN(w[0]) && !Number.isNaN(w[1]))
}

// [[0, 40], [60, 100]] -> "0-40, 60-100"
export function formatWindows(windows) {
  if (!windows || !windows.length) return 'always'
  return windows.map((w) => `${w[0]}-${w[1]}`).join(', ')
}

// "gmp:2099-12-31, iso:2027-06-30" -> { gmp: "2099-12-31", iso: "2027-06-30" }
// A bare "gmp" means no expiry (null).
export function parseQualifications(value) {
  const out = {}
  for (const item of parseList(value)) {
    const idx = item.indexOf(':')
    if (idx === -1) {
      out[item] = null
    } else {
      out[item.slice(0, idx).trim()] = item.slice(idx + 1).trim() || null
    }
  }
  return out
}

// { gmp: "2099-12-31", iso: null } -> "gmp:2099-12-31, iso"
export function formatQualifications(quals) {
  const keys = Object.keys(quals || {})
  if (!keys.length) return '—'
  return keys.map((k) => (quals[k] ? `${k}:${quals[k]}` : k)).join(', ')
}
