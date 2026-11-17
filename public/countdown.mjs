// The campaign includes the whole of 31 December 2027 in Europe/Berlin.
export const DEADLINE = Date.parse('2028-01-01T00:00:00+01:00');
export function remaining(now) {
  const seconds = Math.max(0, Math.ceil((DEADLINE - now) / 1000));
  return {days: Math.floor(seconds / 86400), minutes: Math.floor(seconds % 86400 / 60), seconds: seconds % 60, ended: now >= DEADLINE};
}
