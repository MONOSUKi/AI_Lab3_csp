# Artificial Intelligence Programming Assignment 3  
## Constraint Satisfaction Problems (CSPs): Sudoku Solver

รหัสนักศึกษา: 65200084\
ภาควิชา: Computer Engineering

---

# 1. วิธีการใช้งานโปรแกรม (How to Use)

โปรแกรมนี้เป็นตัวแก้ปัญหา Sudoku โดยใช้แนวคิด **Constraint Satisfaction Problem (CSP)**  
รองรับการใช้งานผ่าน Command Line

## 1.1 รูปแบบคำสั่งพื้นฐาน

```bash
python solver.py <mode>
```

โดย `<mode>` ต้องเป็นหนึ่งในตัวเลือกต่อไปนี้:

* `easy`
* `medium`
* `hard`

ตัวอย่าง:
```bash
python solver.py easy
python solver.py medium
python solver.py hard
```

## 1.2 เปิด/ปิด Heuristic และ Inference

สามารถเลือกเปิดใช้งาน:
* `--mrv` → เปิดใช้ Minimum Remaining Values heuristic
* `--inference`→ เปิดใช้ Forward Checking (Inference)

ตัวอย่าง:
```bash
python solver.py hard --mrv
python solver.py hard --inference
python solver.py hard --mrv --inference
```

## 1.3 โหมด Benchmark

ใช้สำหรับเปรียบเทียบประสิทธิภาพของแต่ละเทคนิค

```bash
python solver.py <mode> --benchmark --runs <จำนวนรอบ>
```

ตัวอย่าง:

```bash
python solver.py hard --benchmark --runs 10
```

ค่าเริ่มต้นของ `--runs` คือ 5 หากไม่ระบุ

---

# 2. แนวคิดที่ใช้ในโปรแกรม
## 2.1 การสร้างแบบจำลอง CSP

ปัญหา Sudoku ถูกกำหนดในรูปแบบ:

CSP = (X, D, C)

* X (Variables): เซลล์ทั้ง 81 ช่องของ Sudoku
* D (Domains): ค่า {1-9}
* C (Constraints):
    * ห้ามซ้ำในแถว
    * ห้ามซ้ำในคอลัมน์
    * ห้ามซ้ำในบล็อก 3x3

## 2.2 Backtracking Search
ใช้ Recursive Backtracking Algorithm เพื่อค้นหาคำตอบ

## 2.3 Heuristic ที่ใช้
### 1) Minimum Remaining Values (MRV)

เลือกตัวแปรที่มีจำนวนค่าที่เป็นไปได้เหลือน้อยที่สุดก่อน
ช่วยลดขนาด Search Tree

### 2) Forward Checking (Inference)

ลบค่าที่ขัดแย้งออกจาก Domain ของตัวแปรข้างเคียงทันที
ช่วยลด Branch ที่ไม่จำเป็น

---

# 3. ผลการทดลอง (Benchmark Results)

ทดลองรัน 10 รอบในแต่ละระดับความยาก

## 3.1 Hard Mode

```
--- No MRV, No Inference ---
Average Backtracks: 143.90
Average Time: 0.0048 sec

--- MRV Only ---
Average Backtracks: 44.60
Average Time: 0.0018 sec

--- Inference Only ---
Average Backtracks: 53.10
Average Time: 0.0024 sec

--- MRV + Inference ---
Average Backtracks: 54.90
Average Time: 0.0028 sec

## 3.2 Medium Mode

```
--- No MRV, No Inference ---
Average Backtracks: 14.90
Average Time: 0.0008 sec

--- MRV Only ---
Average Backtracks: 13.40
Average Time: 0.0012 sec

--- Inference Only ---
Average Backtracks: 16.70
Average Time: 0.0006 sec

--- MRV + Inference ---
Average Backtracks: 12.70
Average Time: 0.0010 sec

## 3.3 Easy Mode

```
--- No MRV, No Inference ---
Average Backtracks: 0.10
Average Time: 0.0002 sec

--- MRV Only ---
Average Backtracks: 0.10
Average Time: 0.0005 sec

--- Inference Only ---
Average Backtracks: 0.10
Average Time: 0.0004 sec

--- MRV + Inference ---
Average Backtracks: 0.10
Average Time: 0.0006 sec

---

# 4. การวิเคราะห์ผล
จากผลการทดลองพบว่า:
1. ในระดับ Easy และ Medium
    * ปัญหามีข้อจำกัดเพียงพออยู่แล้ว
    * จำนวน Backtracks ต่ำมาก
    * Heuristic ไม่ได้ช่วยอย่างมีนัยสำคัญ
2. ในระดับ Hard จะเห็นความแตกต่างชัดเจนที่สุด
    * ลดจำนวน Backtracks อย่างมหาศาล: เมื่อใช้ MRV Only จำนวนการย้อนรอย (Backtracks) ลดลงจาก 143.90 เหลือเพียง 44.60 (ลดลงประมาณ 69%)
    * ความเร็วเพิ่มขึ้น: เวลาเฉลี่ยลดลงจาก 0.0048 วินาที เหลือ 0.0018 วินาที ซึ่งสอดคล้องกับจำนวน Backtracks ที่น้อยลง ทำให้ Algorithm ไม่ต้องเสียเวลาสำรวจกิ่งก้าน (Branch) ที่ไม่นำไปสู่       คำตอบ
3. จากผลลัพธ์ที่ได้
    * Heuristic ไม่ได้ลด Backtracks อย่างชัดเจนในทุกกรณี
    * อาจเกิดจาก Sudoku ที่สร้างขึ้นมีโครงสร้างที่ไม่ซับซ้อนมากพอ
    * ควรเพิ่มระดับความยาก (เช่น เพิ่มจำนวนช่องว่างเป็น 60+) เพื่อให้เห็นผลกระทบของ MRV ชัดเจนขึ้น
