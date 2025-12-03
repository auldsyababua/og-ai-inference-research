# Browser Debugging Guide for 404 Errors

## Quick Browser Console Check

Open your browser's Developer Tools (F12) and check the following:

### 1. Console Tab
Look for JavaScript errors that might indicate the issue:
- Red error messages
- Failed resource loads
- CORS errors
- Authentication errors

### 2. Network Tab
This is the most important for diagnosing 404 errors:

1. **Open Network tab** (F12 → Network)
2. **Clear existing requests** (trash icon)
3. **Try to access the notebook** (click on it in file browser or navigate to URL)
4. **Look for failed requests** (red entries)
5. **Click on the failed request** to see details:
   - **Request URL**: What exact URL was requested?
   - **Status Code**: Is it really 404, or something else?
   - **Response Headers**: What did the server return?
   - **Request Headers**: What was sent?

### Common Issues Found in Network Tab

#### Issue: 404 on `/jupyter/api/contents/...`
**Meaning**: JupyterLab API can't find the file
**Solution**: 
- Check if file exists in container
- Verify file permissions
- Check JupyterLab logs

#### Issue: 401 Unauthorized
**Meaning**: Authentication failed
**Solution**: 
- Check Traefik BasicAuth credentials
- Clear browser cookies for `workhorse.local`
- Try incognito mode

#### Issue: CORS Error
**Meaning**: Cross-origin request blocked
**Solution**: 
- Check Traefik CORS headers
- Verify JupyterLab configuration

#### Issue: 404 on `/jupyter/static/...` or `/jupyter/api/kernelspecs`
**Meaning**: JupyterLab frontend resources missing
**Solution**: 
- Restart JupyterLab container
- Check JupyterLab installation

### 3. Application Tab (Chrome/Edge)
Check:
- **Local Storage**: Any cached data?
- **Session Storage**: Any session data?
- **Cookies**: Any authentication cookies?

### 4. Check Exact URL Being Requested

When you click on the notebook, check what URL appears in the address bar:
- ✅ Correct: `http://workhorse.local/jupyter/lab/tree/work/og-ai-inference-research/tools/unified-calculator.ipynb`
- ❌ Wrong: `http://workhorse.local/jupyter/lab/tree/og-ai-inference-research/tools/unified-calculator.ipynb` (missing `work/`)
- ❌ Wrong: `http://workhorse.local/lab/tree/...` (wrong base path - should be `/jupyter/`)

## Step-by-Step Debugging Process

### Step 1: Check Browser Console
```javascript
// Open console (F12) and run:
console.log('Current URL:', window.location.href);
console.log('JupyterLab API:', window.location.origin + '/jupyter/api');
```

### Step 2: Test JupyterLab API Directly
Open a new tab and try accessing (get token with: `docker exec jupyter jupyter server list`):
```
http://workhorse.local/jupyter/api/contents/work/og-ai-inference-research/tools/unified-calculator.ipynb?token=YOUR_TOKEN
```

Expected: JSON response with notebook content
If 404: File not found by JupyterLab API
If 401: Authentication issue
If 200: File exists, issue is in frontend

### Step 3: Test File Browser API
```
http://workhorse.local/jupyter/api/contents/work/og-ai-inference-research/tools/?token=YOUR_TOKEN
```

Expected: JSON listing of files in tools/ directory
Should include `unified-calculator.ipynb` in the list

### Step 4: Check for Browser Extensions
Some browser extensions can interfere:
- Ad blockers
- Privacy extensions
- Security extensions
- Try disabling extensions or use incognito mode

### Step 5: Clear All Caches
1. **Browser Cache**: Ctrl+Shift+Delete → Clear cached images and files
2. **JupyterLab Cache**: Settings → Advanced Settings → Reset
3. **Hard Reload**: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

## Browser-Specific Instructions

### Chrome/Edge
1. F12 → Network tab
2. Check "Preserve log" checkbox
3. Try accessing notebook
4. Look for red entries
5. Right-click → Copy → Copy as cURL (to see exact request)

### Firefox
1. F12 → Network tab
2. Try accessing notebook
3. Click on failed request
4. Check "Headers" and "Response" tabs

### Safari
1. Enable Developer menu: Preferences → Advanced → Show Develop menu
2. Develop → Show Web Inspector
3. Network tab → Try accessing notebook

## Common Error Messages and Solutions

### "Failed to load resource: the server responded with a status of 404"
**Check Network tab** to see:
- What resource failed to load?
- What was the exact URL?
- Was it the notebook file or a dependency?

### "CORS policy: No 'Access-Control-Allow-Origin' header"
**Solution**: Check Traefik CORS configuration

### "NetworkError when attempting to fetch resource"
**Solution**: 
- Check if JupyterLab container is running
- Check Traefik routing
- Check network connectivity

### "401 Unauthorized"
**Solution**: 
- Check Traefik BasicAuth credentials
- Clear browser cookies
- Try incognito mode

## Testing Checklist

- [ ] Browser console shows no errors
- [ ] Network tab shows successful API calls
- [ ] File appears in JupyterLab file browser
- [ ] Can access `/jupyter/api/contents/work/og-ai-inference-research/tools/unified-calculator.ipynb` directly
- [ ] File listing API shows the notebook
- [ ] Test notebook (`test-notebook.ipynb`) opens successfully
- [ ] Other notebooks in same directory open successfully
- [ ] Hard refresh (Ctrl+Shift+R) doesn't fix it
- [ ] Incognito mode doesn't fix it
- [ ] Different browser doesn't fix it

## If All Else Fails

1. **Capture Network Tab Screenshot**: Show all failed requests
2. **Copy cURL Command**: Right-click failed request → Copy → Copy as cURL
3. **Check Browser Version**: Some older browsers have issues
4. **Try Mobile Browser**: Rule out desktop-specific issues
5. **Check JupyterLab Version**: `docker exec jupyter jupyter --version`

## Reporting Issues

If you need to report this issue, include:
1. Browser and version
2. Screenshot of Network tab showing failed request
3. Exact URL from address bar
4. Console error messages
5. Response from `/jupyter/api/contents/...` API call
6. Whether test-notebook.ipynb works

