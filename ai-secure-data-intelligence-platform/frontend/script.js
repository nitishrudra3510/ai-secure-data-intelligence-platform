// backend url - change this if running on different port
const API_URL = 'http://127.0.0.1:5000/analyze';

// handle file upload - read contents into text area
document.getElementById('fileUpload').addEventListener('change', function(e) {
  var file = e.target.files[0];
  if (!file) return;

  var reader = new FileReader();
  reader.onload = function(event) {
    document.getElementById('logInput').value = event.target.result;
  };
  reader.readAsText(file);
});

// main function - sends log to backend and shows result
async function sendToBackend() {
  var content = document.getElementById('logInput').value;
  var btn = document.getElementById('analyzeBtn');
  var errorDiv = document.getElementById('errorMsg');

  // clear old messages
  errorDiv.style.display = 'none';
  document.getElementById('results').style.display = 'none';

  if (content.trim() === '') {
    showError('Please paste some log content first.');
    return;
  }

  btn.textContent = 'Analyzing...';
  btn.disabled = true;

  try {
    var response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: content })
    });

    if (!response.ok) {
      var errData = await response.json();
      showError(errData.error || 'Server error. Check backend.');
      return;
    }

    var data = await response.json();
    displayResults(data);

  } catch (err) {
    showError('Could not reach backend. Make sure Flask is running on port 5000.');
  } finally {
    btn.textContent = 'Analyze Logs';
    btn.disabled = false;
  }
}

function displayResults(data) {
  document.getElementById('results').style.display = 'block';

  // show risk level with color
  var riskBox = document.getElementById('riskBox');
  var level = data.risk_level || 'LOW';
  var lowerLevel = level.toLowerCase();
  riskBox.className = 'risk-box risk-' + lowerLevel;
  document.getElementById('riskLevel').innerHTML = 'Risk Level:' +
    ' <span class="risk-label risk-' + lowerLevel + '">' + level + '</span>';
  document.getElementById('riskScore').textContent = 'Risk Score: ' + data.risk_score;

  // summary stats
  document.getElementById('totalLines').textContent = data.summary.total_lines;
  document.getElementById('totalFindings').textContent = data.summary.total_findings;

  // insights list
  var ul = document.getElementById('insightsList');
  ul.innerHTML = '';
  data.insights.forEach(function(msg) {
    var li = document.createElement('li');
    li.textContent = msg;
    ul.appendChild(li);
  });

  // findings table
  var tbody = document.getElementById('findingsBody');
  tbody.innerHTML = '';

  if (data.findings.length === 0) {
    document.getElementById('noFindings').style.display = 'block';
    document.getElementById('findingsTable').style.display = 'none';
  } else {
    document.getElementById('noFindings').style.display = 'none';
    document.getElementById('findingsTable').style.display = 'table';

    data.findings.forEach(function(item) {
      var tr = document.createElement('tr');

      // truncate long context text
      var ctx = item.context.length > 60 ? item.context.substring(0, 60) + '...' : item.context;

      tr.innerHTML =
        '<td>' + item.line + '</td>' +
        '<td><span class="badge badge-' + item.type + '">' + item.type + '</span></td>' +
        '<td>' + escapeHtml(item.match) + '</td>' +
        '<td style="font-size:0.78rem;color:#666;">' + escapeHtml(ctx) + '</td>';

      tbody.appendChild(tr);
    });
  }

  // scroll down to results
  document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function showError(msg) {
  var div = document.getElementById('errorMsg');
  div.textContent = msg;
  div.style.display = 'block';
}

// prevent XSS when inserting text into table
function escapeHtml(text) {
  var d = document.createElement('div');
  d.appendChild(document.createTextNode(text));
  return d.innerHTML;
}
