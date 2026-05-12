import os
import shutil
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReportGenerator:
    """Generates an HTML test-execution report under reports/Test Result/."""

    REPORT_DIR = os.path.join(_PROJECT_ROOT, "reports", "Test Result")

    _results: list = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @classmethod
    def add_result(cls, nodeid: str, name: str, status: str,
                   duration: float, screenshot: str | None = None,
                   module: str | None = None) -> None:
        """Append one test result. Call from pytest_runtest_makereport."""
        cls._results.append({
            "nodeid": nodeid,
            "name": name,
            "status": status,
            "duration": round(duration, 2),
            "screenshot": screenshot,
            "module": module,
        })

    @classmethod
    def clear_output_dir(cls) -> None:
        """Delete all previous reports. Call at session start."""
        if os.path.exists(cls.REPORT_DIR):
            for entry in os.scandir(cls.REPORT_DIR):
                try:
                    if entry.is_file() or entry.is_symlink():
                        os.remove(entry.path)
                    elif entry.is_dir():
                        shutil.rmtree(entry.path)
                except OSError:
                    pass
        else:
            os.makedirs(cls.REPORT_DIR, exist_ok=True)

    @classmethod
    def generate(cls) -> str | None:
        """Build and write the HTML report. Returns the file path, or None if no results."""
        if not cls._results:
            return None

        os.makedirs(cls.REPORT_DIR, exist_ok=True)

        now = datetime.now()
        run_time = now.strftime("%Y-%m-%d %H:%M:%S")
        report_path = os.path.join(
            cls.REPORT_DIR, f"test_report_{now.strftime('%Y%m%d_%H%M%S')}.html"
        )

        total = len(cls._results)
        passed = sum(1 for r in cls._results if r["status"] == "PASSED")
        failed = total - passed
        total_duration = round(sum(r["duration"] for r in cls._results), 2)
        pass_pct = round(passed / total * 100, 1) if total else 0.0
        fail_pct = round(failed / total * 100, 1) if total else 0.0

        rows_html = cls._build_rows()
        html = cls._build_html(
            run_time, total, passed, failed,
            total_duration, pass_pct, fail_pct, rows_html,
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)

        return report_path

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @classmethod
    def _build_rows(cls) -> str:
        rows = ""
        for i, r in enumerate(cls._results, 1):
            status_class = "passed" if r["status"] == "PASSED" else "failed"
            badge = f'<span class="badge {status_class}">{r["status"]}</span>'

            module = r.get("module") or (
                r["nodeid"].replace("\\", "/").split("/")[-1].split("::")[0]
                           .replace(".py", "").replace("test_", "")
                           .replace("_", " ").title()
            )

            ss_cell = ""
            if r["screenshot"]:
                ss_cell = (
                    f'<button class="ss-btn" title="View failure screenshot" '
                    f'onclick="openModal(\'../screenshots/{r["screenshot"]}\','
                    f'\'{ r["name"] }\')">'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
                    f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                    f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                    f'<rect x="3" y="3" width="18" height="18" rx="2"/>'
                    f'<circle cx="8.5" cy="8.5" r="1.5"/>'
                    f'<polyline points="21 15 16 10 5 21"/>'
                    f'</svg></button>'
                )

            rows += (
                f"<tr>"
                f"<td class='num'>{i}</td>"
                f"<td class='tname'>{r['name']}</td>"
                f"<td>{module}</td>"
                f"<td>{badge}</td>"
                f"<td>{cls._fmt_duration(r['duration'])}</td>"
                f"<td>{ss_cell}</td>"
                f"</tr>\n"
            )
        return rows

    @staticmethod
    def _fmt_duration(seconds: float) -> str:
        total_sec = int(seconds)
        return f"{total_sec // 60:02d}:{total_sec % 60:02d}"

    @classmethod
    def _build_html(cls, run_time: str, total: int, passed: int, failed: int,
                    total_duration: float, pass_pct: float, fail_pct: float,
                    rows_html: str) -> str:
        total_dur_fmt = cls._fmt_duration(total_duration)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GRC Payroll – Test Report</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',Tahoma,Verdana,sans-serif;background:#f0f2f5;color:#333}}
  .header{{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);color:#fff;padding:28px 40px}}
  .header h1{{font-size:24px;font-weight:600;letter-spacing:.4px}}
  .header p{{margin-top:6px;opacity:.65;font-size:13px}}
  .summary{{display:flex;gap:18px;padding:28px 40px;flex-wrap:wrap}}
  .card{{background:#fff;border-radius:10px;padding:18px 28px;min-width:140px;text-align:center;
         box-shadow:0 2px 8px rgba(0,0,0,.08);border-top:4px solid}}
  .card.total{{border-color:#4a90e2}}.card.pass{{border-color:#27ae60}}.card.fail{{border-color:#e74c3c}}
  .card.pass-pct{{border-color:#1abc9c}}.card.fail-pct{{border-color:#e67e22}}
  .card .count{{font-size:34px;font-weight:700;line-height:1}}
  .card.total .count{{color:#4a90e2}}.card.pass .count{{color:#27ae60}}.card.fail .count{{color:#e74c3c}}
  .card.pass-pct .count{{color:#1abc9c}}.card.fail-pct .count{{color:#e67e22}}
  .card .label{{margin-top:7px;font-size:11px;color:#999;text-transform:uppercase;letter-spacing:1px}}
  tfoot tr{{background:#f8f9fa;border-top:2px solid #eee}}
  tfoot td{{padding:12px 15px;font-size:13px;font-weight:600;color:#555}}
  .tbl-wrap{{margin:0 40px 40px;background:#fff;border-radius:10px;
             box-shadow:0 2px 8px rgba(0,0,0,.08);overflow:hidden}}
  .tbl-head{{padding:16px 22px;border-bottom:1px solid #eee;font-size:15px;font-weight:600}}
  table{{width:100%;border-collapse:collapse}}
  thead th{{background:#f8f9fa;padding:11px 15px;text-align:left;font-size:11px;font-weight:600;
            text-transform:uppercase;letter-spacing:.8px;color:#777;border-bottom:2px solid #eee}}
  tbody tr{{border-bottom:1px solid #f0f0f0;transition:background .12s}}
  tbody tr:hover{{background:#fafbfc}}
  tbody tr:last-child{{border-bottom:none}}
  td{{padding:13px 15px;font-size:13.5px;vertical-align:middle}}
  td.num{{color:#bbb;font-size:12px;width:40px}}
  td.tname{{font-weight:500;color:#222}}
  .badge{{display:inline-block;padding:3px 11px;border-radius:20px;
          font-size:11.5px;font-weight:600;letter-spacing:.4px}}
  .badge.passed{{background:#e8f5e9;color:#2e7d32}}
  .badge.failed{{background:#fdecea;color:#c62828}}
  .ss-btn{{background:#fff8e1;border:1px solid #ffc107;border-radius:6px;padding:5px 9px;
           cursor:pointer;color:#e67e00;display:inline-flex;align-items:center;transition:all .18s}}
  .ss-btn:hover{{background:#ffc107;color:#fff;border-color:#ffc107}}
  .overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);
            z-index:999;align-items:center;justify-content:center}}
  .overlay.on{{display:flex}}
  .modal{{background:#fff;border-radius:12px;max-width:92vw;max-height:92vh;
          overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
  .modal-hdr{{padding:14px 18px;display:flex;justify-content:space-between;
              align-items:center;border-bottom:1px solid #eee}}
  .modal-hdr h3{{font-size:14px;color:#333;max-width:72vw;
                overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  .close-btn{{background:none;border:none;font-size:20px;cursor:pointer;
              color:#aaa;line-height:1;padding:0 3px}}
  .close-btn:hover{{color:#333}}
  #modal-img{{display:block;max-width:88vw;max-height:80vh;object-fit:contain}}
</style>
</head>
<body>
<div class="header">
  <h1>GRC Payroll &mdash; Test Execution Report</h1>
  <p>Generated on {run_time}</p>
</div>
<div class="summary">
  <div class="card total"><div class="count">{total}</div><div class="label">Total</div></div>
  <div class="card pass"><div class="count">{passed}</div><div class="label">Passed</div></div>
  <div class="card fail"><div class="count">{failed}</div><div class="label">Failed</div></div>
  <div class="card pass-pct"><div class="count">{pass_pct}%</div><div class="label">Pass Rate</div></div>
  <div class="card fail-pct"><div class="count">{fail_pct}%</div><div class="label">Fail Rate</div></div>
</div>
<div class="tbl-wrap">
  <div class="tbl-head">Test Results</div>
  <table>
    <thead>
      <tr>
        <th>#</th><th>Test Name</th><th>Module</th>
        <th>Status</th><th>Duration</th><th>Screenshot</th>
      </tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
    <tfoot>
      <tr>
        <td colspan="4" style="text-align:right;letter-spacing:.5px;text-transform:uppercase;font-size:11px;color:#777;">Total Duration</td>
        <td>{total_dur_fmt}</td>
        <td></td>
      </tr>
    </tfoot>
  </table>
</div>
<div class="overlay" id="overlay" onclick="closeOnBg(event)">
  <div class="modal">
    <div class="modal-hdr">
      <h3 id="modal-title">Failure Screenshot</h3>
      <button class="close-btn" onclick="closeModal()">&#x2715;</button>
    </div>
    <img id="modal-img" src="" alt="screenshot">
  </div>
</div>
<script>
  function openModal(src, name) {{
    document.getElementById('modal-img').src = src;
    document.getElementById('modal-title').textContent = 'Failed: ' + name;
    document.getElementById('overlay').classList.add('on');
  }}
  function closeModal() {{
    document.getElementById('overlay').classList.remove('on');
    document.getElementById('modal-img').src = '';
  }}
  function closeOnBg(e) {{
    if (e.target === document.getElementById('overlay')) closeModal();
  }}
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeModal();
  }});
</script>
</body>
</html>"""
