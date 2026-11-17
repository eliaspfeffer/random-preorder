import assert from 'node:assert/strict';
import {DEADLINE, remaining} from '../public/countdown.mjs';
assert.equal(new Date(DEADLINE).toISOString(), '2027-12-31T23:00:00.000Z');
assert.deepEqual(remaining(DEADLINE - 86401000), {days:1, minutes:0, seconds:1, ended:false});
assert.deepEqual(remaining(DEADLINE - 86399000), {days:0, minutes:1439, seconds:59, ended:false});
assert.deepEqual(remaining(DEADLINE - 1), {days:0, minutes:0, seconds:1, ended:false});
assert.deepEqual(remaining(DEADLINE), {days:0, minutes:0, seconds:0, ended:true});
assert.deepEqual(remaining(DEADLINE + 1000), {days:0, minutes:0, seconds:0, ended:true});
console.log('Countdown: 6 deadline and rollover checks passed.');
