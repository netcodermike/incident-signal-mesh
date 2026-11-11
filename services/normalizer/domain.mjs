const severityRank = new Map([['info', 0], ['warning', 1], ['error', 2], ['critical', 3]])

export function operation({ signals }) {
  if (!Array.isArray(signals)) throw new TypeError('Expected signals array')
  return { signals: signals.map(({ id, service, fingerprint, severity }) => {
    if (![id, service, fingerprint, severity].every(value => typeof value === 'string' && value.trim())) {
      throw new TypeError('Each signal needs id, service, fingerprint and severity')
    }
    const level = severity.trim().toLowerCase()
    if (!severityRank.has(level)) throw new TypeError('Unknown severity')
    return { id: id.trim(), service: service.trim().toLowerCase(), fingerprint: fingerprint.trim().toLowerCase(),
      severity: level, rank: severityRank.get(level) }
  }) }
}
