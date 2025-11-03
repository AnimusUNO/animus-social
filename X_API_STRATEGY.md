# X API Strategy: Polling vs Filtered Stream

## Current Implementation: Polling

**How it works:**
- Checks for mentions every 120 seconds (2 minutes)
- Uses `/tweets/search/recent` or `/users/{id}/mentions` endpoints
- Stores `last_seen_id` to avoid duplicates
- Queues mentions for processing

**Pros:**
- ✅ Simple to implement and maintain
- ✅ Works with basic/free API tiers
- ✅ Less complex error handling
- ✅ No persistent connection to maintain
- ✅ Easy to debug and monitor

**Cons:**
- ❌ Higher latency (up to 2 minutes delay)
- ❌ Wastes API calls when there are no mentions
- ❌ Rate limit concerns (varies by tier)
- ❌ Not real-time (poor UX for quick responses)

## Alternative: Filtered Stream

**How it works:**
- Maintains persistent HTTP/WebSocket connection to X API
- Real-time stream of tweets matching filter rules (e.g., `@biancabotx`)
- Immediate notification when mentions occur
- Uses `/2/tweets/search/stream` endpoint

**Pros:**
- ✅ Real-time responses (better UX)
- ✅ More efficient (no wasted polling calls)
- ✅ Better for high-volume scenarios
- ✅ Lower latency = better user experience

**Cons:**
- ❌ Requires persistent connection management
- ❌ More complex error handling (reconnection logic)
- ❌ May require paid/higher API tier
- ❌ Connection stability concerns
- ❌ More complex to implement and debug

## Recommendation: **Hybrid Approach**

### Phase 1: **Keep Polling (Current)** ✅
**Why:**
- It's already working
- Simple and reliable
- Good enough for MVP/early testing
- No infrastructure changes needed

**Improvements to make:**
1. Reduce poll interval to 60 seconds (better balance)
2. Implement proper rate limit tracking
3. Add exponential backoff on rate limit errors
4. Add monitoring/alerts for missed mentions

### Phase 2: **Add Filtered Stream** (Future Enhancement)
**When to implement:**
- When you need sub-minute response times
- If you're on a paid API tier that supports streams
- If polling rate limits become a bottleneck
- If you have high mention volume

**Implementation strategy:**
1. Keep polling as fallback/backup
2. Implement stream connection with auto-reconnect
3. Use stream for primary, polling as safety net
4. Monitor both and compare performance

## Specific Recommendation for Animus Social

### For Bianca Now: **Stick with Polling**
**Reasons:**
1. **Reliability** > Speed for social media bots
2. 60-120 second response time is acceptable for Twitter interactions
3. Simpler = fewer failure points
4. Can optimize polling first (shorter intervals, better rate limit handling)

### When to Switch to Stream:
- You upgrade to a paid X API tier with stream access
- You need <30 second response times
- Mention volume >10/hour consistently
- You have dedicated infrastructure for connection management

## Implementation Priority

1. **Immediate**: Optimize current polling
   - Reduce to 60s interval
   - Better rate limit handling
   - Monitoring improvements

2. **Short-term**: Hybrid polling
   - Smart interval (adjust based on mention frequency)
   - Adaptive delays (longer when quiet, shorter when active)

3. **Long-term**: Stream support
   - Implement filtered stream
   - Keep polling as backup
   - Monitor and compare

## Code Example: Improved Polling

```python
# Adaptive polling based on activity
if recent_mentions_count > 0:
    FETCH_DELAY_SEC = 30  # More frequent when active
else:
    FETCH_DELAY_SEC = 120  # Less frequent when quiet

# Rate limit tracking
rate_limit_remaining = response.headers.get('x-rate-limit-remaining', 0)
if int(rate_limit_remaining) < 10:
    FETCH_DELAY_SEC *= 2  # Slow down when approaching limit
```

## Conclusion

**Start with optimized polling.** It's proven, reliable, and sufficient for most use cases. Add streaming later if needed, but don't over-engineer for your current needs.

**The best code is the code that works reliably.** Polling works. Streams add complexity. Only add complexity when you have a clear need.

