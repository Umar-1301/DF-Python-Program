# Forensic Image Analysis Tool

This repository contains a Python-based forensic image analysis tool developed for the Advanced Programming for Digital Forensics module at University. The tool performs detailed forensic image analysis, enabling users to discover partition layouts, analyze file systems, and generate comprehensive reports in JSON format.

---

## **Project Overview**
The tool is designed to streamline forensic investigations by providing efficient methods for analyzing disk images and extracting critical information. Using the `pytsk3` library, the program interfaces directly with forensic images to explore their structures and metadata.

### **Key Features**
1. **Partition Analysis**:
   - Identifies partition layouts (MBR or GPT).
   - Displays detailed information about each partition, including file system type, start sector, and total allocated space.

2. **File System Analysis**:
   - Allows selection of a partition for deeper analysis.
   - Extracts metadata for files and directories, including MD5 hash values for integrity verification.

3. **Report Generation**:
   - Creates structured reports in JSON format for partition details and file system analysis.

4. **User-Friendly CLI**:
   - Interactive menu options for discovering partitions, analyzing file systems, and generating reports.

---

## **Technologies Used**
- **Python**: Core programming language.
- **pytsk3**: Forensic library for disk image and file system analysis.
- **hashlib**: Generates MD5 hash values for file verification.
- **json**: Facilitates structured and readable report generation.

---

