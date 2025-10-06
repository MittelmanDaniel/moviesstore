# 🗺️ Local Popularity Map - Testing Guide

## ✅ Feature Successfully Implemented!

The Local Popularity Map feature is now live and ready to test. This guide will walk you through all the completion steps.

---

## 🚀 Quick Start

### Server is Running
- URL: http://127.0.0.1:8000/
- Map URL: http://127.0.0.1:8000/analytics/

### Test Accounts Created
All test users have password: `testpass123`

| Username | Region | Orders Created |
|----------|--------|----------------|
| user_ga | Georgia | 2-5 orders |
| user_ca | California | 2-5 orders |
| user_ny | New York | 2-5 orders |
| user_tx | Texas | 2-5 orders |
| user_fl | Florida | 2-5 orders |
| user_il | Illinois | 2-5 orders |
| user_wa | Washington | 2-5 orders |
| user_ma | Massachusetts | 2-5 orders |

---

## 📋 Completion Steps Testing

### **Step a) Log in or register an account** ✅

**Option 1: Login with test account**
1. Go to http://127.0.0.1:8000/accounts/login/
2. Login with:
   - Username: `user_ga`
   - Password: `testpass123`

**Option 2: Create new account**
1. Go to http://127.0.0.1:8000/accounts/signup/
2. Fill in:
   - Username: (your choice)
   - Password: (your choice)
   - **Region**: Select a state from dropdown
3. Click "Sign Up"
4. Login with your credentials

---

### **Step b) Navigate to "Local Popularity Map" page** ✅

**Method 1: Via Navigation**
- Click "Popularity Map" in the top navigation bar

**Method 2: Direct URL**
- Go to http://127.0.0.1:8000/analytics/

---

### **Step c) Verify map loads correctly with regional boundaries/markers** ✅

**What to check:**
- [ ] Map displays centered on United States
- [ ] Red circular markers appear on states with purchases
- [ ] Markers show state codes (GA, CA, NY, TX, FL, IL, WA, MA)
- [ ] Marker size varies based on purchase volume
- [ ] Map is interactive (can zoom and pan)

**Expected behavior:**
- You should see 8 red markers (one for each test user's state)
- Larger markers = more purchases in that region
- All markers have state code labels

---

### **Step d) Confirm trending movies displayed in at least one region** ✅

**How to test:**
1. **Hover** over any red marker on the map
2. **Click** on a marker (e.g., GA, CA, NY, TX)
3. A popup window will appear

**What to verify:**
- [ ] Popup shows state name
- [ ] "Top Trending Movies" list is displayed
- [ ] Each movie shows:
  - Movie title
  - Purchase count (e.g., "5 purchases")
- [ ] At least 1-3 movies are listed

**Example popup content:**
```
Georgia
Top Trending Movies:
1. Inception (8 purchases)
2. Avatar (5 purchases)
3. Titanic (3 purchases)

[View Full Details] button
```

---

### **Step e) Select a specific region on the map** ✅

**How to test:**
1. Click on any marker (e.g., California - CA)
2. In the popup, click **"View Full Details"** button
3. You'll be redirected to the region detail page

**Alternative method:**
- Direct URL: http://127.0.0.1:8000/analytics/region/CA/
- Replace CA with any state code (GA, NY, TX, FL, etc.)

---

### **Step f) Verify region's top trending movies are listed** ✅

**On the region detail page, verify:**
- [ ] Page title shows "Trending in [State Name]"
- [ ] Breadcrumb navigation appears at top
- [ ] Table displays:
  - **Rank** (#1, #2, #3, etc.)
  - **Movie name**
  - **Total purchases** in last 30 days
  - **Unique buyers** count
  - **"View Details"** button for each movie
- [ ] Up to 10 movies are shown

**Example table:**

| Rank | Movie | Purchases | Unique Buyers | Action |
|------|-------|-----------|---------------|--------|
| #1 | Inception | 12 | 5 | [View Details] |
| #2 | Avatar | 8 | 4 | [View Details] |
| #3 | Titanic | 6 | 3 | [View Details] |

---

### **Step g) Compare with your own purchases to ensure accuracy** ✅

**If logged in as test user:**
1. On the region detail page, look at the right sidebar
2. Find "Your Recent Purchases" card
3. This shows YOUR purchases from last 30 days

**How to verify accuracy:**
1. Login as `user_ga` (password: `testpass123`)
2. Go to http://127.0.0.1:8000/accounts/orders/
3. Note which movies you purchased
4. Visit http://127.0.0.1:8000/analytics/region/GA/
5. Check if:
   - Your purchased movies appear in the trending list
   - The "Your Recent Purchases" sidebar shows your movies
   - Purchase counts are accurate

**Cross-check with another user:**
1. Logout
2. Login as `user_ca` (password: `testpass123`)
3. Visit California region: http://127.0.0.1:8000/analytics/region/CA/
4. Verify different trending movies appear
5. Check "Your Recent Purchases" shows California user's data

---

## 🎯 Additional Testing Scenarios

### Test Case 1: Region with No Data
1. Visit a state with no test users (e.g., Montana)
2. URL: http://127.0.0.1:8000/analytics/region/MT/
3. Expected: "No trending data available for this region yet."

### Test Case 2: Create New Purchase
1. Login as any test user
2. Go to http://127.0.0.1:8000/movies/
3. Add a movie to cart and purchase
4. Return to analytics map
5. Expected: Your region's marker may grow, trending count increases

### Test Case 3: Sign Up with Region
1. Logout
2. Go to http://127.0.0.1:8000/accounts/signup/
3. Create account with region = "Nevada"
4. Make some purchases
5. Visit http://127.0.0.1:8000/analytics/region/NV/
6. Expected: Your purchases appear in Nevada's trending list

---

## 🔍 Technical Details

### Data Scope
- **Time Range**: Last 30 days
- **Aggregation**: Sum of quantities purchased per movie per region
- **Display**: Top 5 on map popup, Top 10 on detail page

### API Endpoint
- URL: http://127.0.0.1:8000/analytics/api/regional-data/
- Returns JSON with all regional trending data
- Used by map to render markers

### Database Tables
- `analytics_region` - 50 US states
- `analytics_userprofile` - User location data
- Queries join: Order → Item → Movie + User → Profile → Region

---

## 🛠️ Commands Used

### Seed Data (Already Run)
```bash
python manage.py seed_regions      # Created 50 states
python manage.py seed_test_data    # Created 8 users + 27 orders
```

### Re-seed if Needed
```bash
# Clear and re-create test data
python manage.py flush --no-input
python manage.py migrate
python manage.py seed_regions
python manage.py seed_test_data
```

---

## 📊 Expected Results Summary

✅ **All completion steps should pass:**

| Step | Description | Status |
|------|-------------|--------|
| a | Login/Register | ✅ Works |
| b | Navigate to map | ✅ Link in navbar |
| c | Map loads with markers | ✅ 8 state markers |
| d | Trending movies displayed | ✅ In popups |
| e | Select region | ✅ Click markers |
| f | View detailed trending list | ✅ Table with top 10 |
| g | Compare with own purchases | ✅ Sidebar + accuracy |

---

## 🎨 Features Implemented

- ✅ US States-based regions (50 states)
- ✅ Interactive Leaflet.js map
- ✅ Dynamic marker sizing based on purchase volume
- ✅ Region selection via map clicks
- ✅ Detailed trending statistics page
- ✅ User purchase comparison
- ✅ Last 30 days data scope
- ✅ Automatic region capture during signup
- ✅ Bootstrap 5 responsive design
- ✅ Navigation integration

---

## 🐛 Troubleshooting

### Issue: No markers appear on map
**Solution**: Check browser console for errors. Ensure you ran `seed_test_data` command.

### Issue: "No trending data" message
**Solution**: Normal for states without test users. Try states: GA, CA, NY, TX, FL, IL, WA, MA

### Issue: Can't see own purchases
**Solution**: You must be logged in. Check if you have orders in last 30 days.

---

## 🎉 Success Criteria

Your implementation is **COMPLETE** if:
- [x] Map displays on /analytics/
- [x] 8 states show red markers
- [x] Clicking markers shows trending movies
- [x] Detail pages show top 10 movies with accurate counts
- [x] Logged-in users see their own purchases
- [x] New signups can select their region
- [x] All test users can access their regional data

---

## 📝 Next Steps (Optional Enhancements)

1. **Add filtering**: Filter by time range (7 days, 30 days, all time)
2. **Add charts**: Visualize trending data with Chart.js
3. **Add heat map**: Show intensity of purchases by color
4. **Add search**: Search for specific movies in regions
5. **Add notifications**: Alert users when their region's trending changes
6. **Add caching**: Cache regional data for performance

---

**Happy Testing! 🎬🗺️**
