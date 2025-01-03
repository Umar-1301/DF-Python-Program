# Code Overview: Forensic Image Analysis Tool

This document provides a detailed explanation of the code structure, functions, and logic.

---

## **1. File: `forensic_tool.py`**

### **Main Functions**
1. **`main()`**:
   - Acts as the entry point for the program.
   - Displays a menu with options for partition discovery, file analysis, and report generation.

2. **`discover_partitions(image, disk)`**:
   - Analyzes the partition layout.
   - Prints a formatted table of partition details, including start sector and total allocated space.

3. **`select_partition(image, disk)`**:
   - Prompts the user to select a partition for analysis.
   - Iterates through files in the selected partition, calculating MD5 hashes for files.
   - Highlights matching hashes against user-specified input.

4. **`create_report(image, disk)`**:
   - Generates a JSON report with partition and file system details.
   - Writes the report to a user-specified file.

---

## **2. Key Libraries**
- **pytsk3**:
  - Interfaces with forensic image files.
  - Extracts partition and file system details.
- **hashlib**:
  - Computes MD5 hash values for files.
- **json**:
  - Formats and writes output data to structured files.

---

## **3. Example Workflow**
1. User inputs forensic image file (e.g., `test.dd`).
2. Program discovers partition layout and displays a table.
3. User selects a partition to analyze.
4. File metadata and hash values are displayed.
5. Program generates a JSON report summarizing findings.

---

## **4. Challenges Addressed**
- **Unsupported Partitions**:
  - Handled gracefully with exception handling.
- **Large Files**:
  - Processed in memory-efficient chunks to avoid performance bottlenecks.
- **Report Clarity**:
  - Designed nested JSON structures for intuitive output.

---

## **5. Future Improvements**
- Extend support for additional forensic image formats (e.g., VMDK, E01).
- Integrate advanced forensic features, such as OS artifact analysis.
- Implement a graphical user interface (GUI) for enhanced usability.

