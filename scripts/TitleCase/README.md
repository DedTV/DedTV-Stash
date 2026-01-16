
## **Stash Scene Title Formatter**

This utility automates the process of converting messy or inconsistent scene titles (e.g., `SCENE IN ALL CAPS` or `scene in lowercase`) into a clean, standardized **Title Case** format.

### **Core Functions**

* **Smart Title Casing:** Uses the `titlecase` library to intelligently capitalize titles. It follows professional style guidelines, ensuring that articles and prepositions are lowercase while primary words are capitalized.
* **Acronym Preservation:** Features a built-in whitelist for common acronyms (e.g., `USA`, `FBI`, `CIA`, `DP`). This prevents the script from incorrectly formatting these as `Usa` or `Fbi`.
* **Efficient Updating:** The script performs a "check-before-write" operation. It fetches all titles but only executes an `UPDATE` command if the formatted title actually differs from the original, reducing unnecessary database strain.
* **Progress Tracking:** Includes a real-time console output that displays which scenes are being updated, a progress counter for large libraries, and a final summary of changes.
* **Error Handling & Safety:**
* **Automatic Rollback:** If a database error occurs mid-process, the script rolls back changes to prevent database corruption.
* **Dictionary Cursors:** Uses `sqlite3.Row` for reliable column mapping.
* **Empty Title Handling:** Gracefully skips scenes with missing or null titles.



### **Technical Requirements**

To use this script, you must have the `titlecase` library installed:

```bash
pip install titlecase

```

### **Configuration**

Before running, update the `DATABASE_FILE` variable in the script to point to your specific Stash database location:

```python
DATABASE_FILE = r'E:\stash-go.sqlite'

```
