<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบแดชบอร์ดบริหารทรัพยากรบุคคล (HR Analytics Dashboard)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Google Fonts (Sarabun & Inter) -->
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Sarabun', 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        /* Custom scrollbar for data table */
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- Navbar -->
    <header class="bg-indigo-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="p-2 bg-indigo-700 rounded-lg">
                    <i data-lucide="users" class="w-6 h-6 text-indigo-200"></i>
                </div>
                <div>
                    <h1 class="text-lg sm:text-xl font-bold tracking-tight">ระบบวิเคราะห์ข้อมูลทรัพยากรบุคคล</h1>
                    <p class="text-xs text-indigo-200 hidden sm:block">HR Analytics & Employment Status Dashboard</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button id="reset-data-btn" class="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-indigo-800 hover:bg-indigo-700 text-indigo-100 transition shadow-sm border border-indigo-600">
                    <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 mr-1.5"></i>
                    โหลดข้อมูลตัวอย่าง
                </button>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- Upload & Notification Bar -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 bg-white rounded-xl p-5 shadow-sm border border-slate-200 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h2 class="text-base font-semibold text-slate-800 flex items-center">
                            <i data-lucide="file-up" class="w-5 h-5 mr-2 text-indigo-600"></i>
                            นำเข้าข้อมูล HR (Upload File)
                        </h2>
                        <span id="data-source-badge" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
                            ข้อมูลตัวอย่าง (Sample Data)
                        </span>
                    </div>
                    <p class="text-xs text-slate-500 mb-4">รองรับไฟล์ข้อมูล HR DATA.txt (Format แบบ TSV/Tab-delimited) หรือไฟล์ CSV / TSV ทั่วไป</p>
                </div>
                
                <div class="flex flex-col sm:flex-row gap-3 items-center">
                    <label class="w-full flex-1 flex items-center justify-center px-4 py-2.5 bg-slate-50 border-2 border-dashed border-indigo-200 rounded-lg cursor-pointer hover:bg-indigo-50/50 hover:border-indigo-400 transition group text-center">
                        <i data-lucide="upload-cloud" class="w-5 h-5 text-indigo-500 mr-2 group-hover:scale-110 transition-transform"></i>
                        <span class="text-xs font-medium text-slate-600 group-hover:text-indigo-700">คลิกเพื่อเลือกไฟล์ HR DATA.txt หรือ CSV</span>
                        <input type="file" id="file-input" accept=".txt,.csv,.tsv" class="hidden" />
                    </label>
                </div>
            </div>

            <!-- Quick Filter Summary Box -->
            <div class="bg-gradient-to-br from-indigo-50 to-slate-50 rounded-xl p-5 shadow-sm border border-indigo-100 flex flex-col justify-between">
                <div>
                    <h3 class="text-sm font-semibold text-indigo-900 mb-2 flex items-center">
                        <i data-lucide="info" class="w-4 h-4 mr-1.5 text-indigo-600"></i>
                        สถานะข้อมูลปัจจุบัน
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed mb-3">
                        ข้อมูลกำลังแสดงสถิติสถานะพนักงาน (Employment Status) แยกตามรายแผนก (Department)
                    </p>
                </div>
                <div class="pt-2 border-t border-indigo-100/60 flex justify-between text-xs text-slate-500">
                    <span>จำนวนเรคคอร์ดทั้งหมด:</span>
                    <span id="total-rows-count" class="font-bold text-indigo-700">0 รายการ</span>
                </div>
            </div>
        </div>

        <!-- KPI Cards Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <!-- Card 1: Total Employees -->
            <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative overflow-hidden">
                <div class="absolute -right-2 -bottom-2 opacity-10 text-slate-800">
                    <i data-lucide="users" class="w-20 h-20"></i>
                </div>
                <p class="text-xs font-medium text-slate-500 mb-1">พนักงานทั้งหมด</p>
                <h3 id="kpi-total" class="text-2xl font-bold text-slate-800">0</h3>
                <span class="text-[10px] text-slate-400">บุคลากรในระบบ</span>
            </div>

            <!-- Card 2: Active -->
            <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative overflow-hidden border-l-4 border-l-blue-500">
                <div class="absolute -right-2 -bottom-2 opacity-10 text-blue-600">
                    <i data-lucide="user-check" class="w-20 h-20"></i>
                </div>
                <p class="text-xs font-medium text-slate-500 mb-1">ทำงานอยู่ (Active)</p>
                <h3 id="kpi-active" class="text-2xl font-bold text-blue-600">0</h3>
                <span id="kpi-active-pct" class="text-[10px] font-semibold text-blue-500">0% ของทั้งหมด</span>
            </div>

            <!-- Card 3: Voluntarily Terminated -->
            <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative overflow-hidden border-l-4 border-l-amber-500">
                <div class="absolute -right-2 -bottom-2 opacity-10 text-amber-600">
                    <i data-lucide="user-minus" class="w-20 h-20"></i>
                </div>
                <p class="text-xs font-medium text-slate-500 mb-1">ลาออกเอง (Voluntary)</p>
                <h3 id="kpi-voluntary" class="text-2xl font-bold text-amber-600">0</h3>
                <span id="kpi-voluntary-pct" class="text-[10px] font-semibold text-amber-500">0% ของทั้งหมด</span>
            </div>

            <!-- Card 4: Terminated for Cause -->
            <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative overflow-hidden border-l-4 border-l-rose-500">
                <div class="absolute -right-2 -bottom-2 opacity-10 text-rose-600">
                    <i data-lucide="user-x" class="w-20 h-20"></i>
                </div>
                <p class="text-xs font-medium text-slate-500 mb-1">ให้ออก/เลิกจ้าง (Cause)</p>
                <h3 id="kpi-cause" class="text-2xl font-bold text-rose-600">0</h3>
                <span id="kpi-cause-pct" class="text-[10px] font-semibold text-rose-500">0% ของทั้งหมด</span>
            </div>

            <!-- Card 5: Leave / Future Start -->
            <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 relative overflow-hidden border-l-4 border-l-emerald-500 col-span-2 md:col-span-1">
                <div class="absolute -right-2 -bottom-2 opacity-10 text-emerald-600">
                    <i data-lucide="calendar" class="w-20 h-20"></i>
                </div>
                <p class="text-xs font-medium text-slate-500 mb-1">ลาพัก / รอเริ่มงาน</p>
                <h3 id="kpi-other" class="text-2xl font-bold text-emerald-600">0</h3>
                <span class="text-[10px] text-slate-400">Leave of Absence & Future</span>
            </div>
        </div>

        <!-- Controls & Filters -->
        <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200 flex flex-wrap gap-4 items-center justify-between">
            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                <div class="flex items-center text-xs font-semibold text-slate-600 mr-2">
                    <i data-lucide="filter" class="w-4 h-4 mr-1 text-indigo-600"></i>
                    ตัวกรองข้อมูล:
                </div>

                <!-- Filter Department -->
                <div class="min-w-[160px]">
                    <select id="filter-dept" class="w-full text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                        <option value="ALL">-- ทุกแผนก (All Departments) --</option>
                    </select>
                </div>

                <!-- Filter Status -->
                <div class="min-w-[160px]">
                    <select id="filter-status" class="w-full text-xs bg-slate-50 border border-slate-300 text-slate-700 rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                        <option value="ALL">-- ทุกสถานะ (All Statuses) --</option>
                    </select>
                </div>

                <button id="clear-filters-btn" class="px-3 py-2 text-xs font-medium text-slate-600 hover:text-indigo-600 bg-slate-100 hover:bg-indigo-50 rounded-lg transition">
                    ล้างตัวกรอง
                </button>
            </div>

            <div class="text-xs text-slate-400 italic w-full md:w-auto text-right">
                * กราฟและตารางจะอัปเดตอัตโนมัติตามตัวกรอง
            </div>
        </div>

        <!-- Chart Section -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-200">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                <div>
                    <h2 class="text-base font-bold text-slate-800 flex items-center">
                        <i data-lucide="bar-chart-3" class="w-5 h-5 mr-2 text-indigo-600"></i>
                        Employment Status by Department
                    </h2>
                    <p class="text-xs text-slate-500">เปรียบเทียบจำนวนสัดส่วนสถานะการทำงานของพนักงานจำแนกตามรายแผนก</p>
                </div>
            </div>

            <!-- Chart Canvas Container -->
            <div class="relative w-full h-[360px] sm:h-[420px]">
                <canvas id="deptStatusChart"></canvas>
            </div>
        </div>

        <!-- Data Table Section -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="p-4 bg-slate-50/50 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div class="flex items-center space-x-2">
                    <i data-lucide="table" class="w-5 h-5 text-indigo-600"></i>
                    <h3 class="text-sm font-bold text-slate-800">รายการข้อมูลพนักงาน (Employee Records)</h3>
                    <span id="filtered-count-badge" class="px-2 py-0.5 text-xs font-semibold bg-indigo-100 text-indigo-700 rounded-full">0 รายการ</span>
                </div>

                <!-- Table Search Box -->
                <div class="relative w-full sm:w-64">
                    <i data-lucide="search" class="w-4 h-4 absolute left-3 top-2.5 text-slate-400"></i>
                    <input type="text" id="search-input" placeholder="ค้นหาชื่อ, แผนก, ตำแหน่ง..." class="w-full pl-9 pr-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                </div>
            </div>

            <!-- Table Body -->
            <div class="overflow-x-auto max-h-[400px] custom-scrollbar">
                <table class="w-full text-xs text-left text-slate-600">
                    <thead class="text-[11px] text-slate-500 uppercase bg-slate-100 sticky top-0 border-b border-slate-200">
                        <tr>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('EmpID')">
                                ID <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('Employee_Name')">
                                ชื่อ-นามสกุล <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('Department')">
                                แผนก (Department) <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('Position')">
                                ตำแหน่ง (Position) <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('EmploymentStatus')">
                                สถานะการทำงาน <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                            <th scope="col" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 transition" onclick="sortTable('Sex')">
                                เพศ <i data-lucide="arrow-up-down" class="w-3 h-3 inline text-slate-400"></i>
                            </th>
                        </tr>
                    </thead>
                    <tbody id="table-body" class="divide-y divide-slate-100">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
            
            <!-- Table Footer Pagination/Info -->
            <div class="px-4 py-2 bg-slate-50 border-t border-slate-200 text-xs text-slate-500 flex justify-between items-center">
                <span id="table-showing-info">กำลังแสดงข้อมูล 0 จาก 0 รายการ</span>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 mt-8 text-center text-xs text-slate-500">
        <p>© 2026 HR Analytics System - ระบบแดชบอร์ดบริหารข้อมูลทรัพยากรบุคคล</p>
    </footer>

    <script>
        // Color Palette definitions matching the benchmark chart
        const STATUS_COLORS = {
            'Active': { bg: '#1f77b4', border: '#1f77b4', badge: 'bg-blue-100 text-blue-800' },
            'Future Start': { bg: '#ff7f0e', border: '#ff7f0e', badge: 'bg-orange-100 text-orange-800' },
            'Leave of Absence': { bg: '#2ca02c', border: '#2ca02c', badge: 'bg-green-100 text-green-800' },
            'Voluntarily Terminated': { bg: '#d62728', border: '#d62728', badge: 'bg-red-100 text-red-800' },
            'Terminated for Cause': { bg: '#9467bd', border: '#9467bd', badge: 'bg-purple-100 text-purple-800' }
        };

        const DEFAULT_COLOR = { bg: '#8c564b', border: '#8c564b', badge: 'bg-slate-100 text-slate-800' };

        // Built-in Sample Dataset representing classic HR DATA.txt
        const SAMPLE_HR_DATA = [
            { EmpID: "1001", Employee_Name: "Brown, Mia", Department: "Admin Offices", Position: "Accountant I", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1002", Employee_Name: "LaPierre, Jose", Department: "Admin Offices", Position: "Executive Assistant", EmploymentStatus: "Voluntarily Terminated", Sex: "M" },
            { EmpID: "1003", Employee_Name: "Steciuk, Nicholas", Department: "Admin Offices", Position: "Shared Services Manager", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1004", Employee_Name: "Howard, Case", Department: "Executive Office", Position: "President & CEO", EmploymentStatus: "Active", Sex: "M" },
            
            // IT/IS
            { EmpID: "1005", Employee_Name: "Fidelia, Jamel", Department: "IT/IS", Position: "IT Manager - DB", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1006", Employee_Name: "Desimone, Carl", Department: "IT/IS", Position: "Senior BI Developer", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1007", Employee_Name: "Gozard, Bruce", Department: "IT/IS", Position: "Database Administrator", EmploymentStatus: "Voluntarily Terminated", Sex: "M" },
            { EmpID: "1008", Employee_Name: "Monroe, Brenda", Department: "IT/IS", Position: "Network Engineer", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1009", Employee_Name: "Davenport, David", Department: "IT/IS", Position: "IT Support", EmploymentStatus: "Terminated for Cause", Sex: "M" },
            { EmpID: "1010", Employee_Name: "Soto, Julia", Department: "IT/IS", Position: "IT Support", EmploymentStatus: "Leave of Absence", Sex: "F" },

            // Software Engineering
            { EmpID: "1011", Employee_Name: "Andreola, Colby", Department: "Software Engineering", Position: "Software Engineer", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1012", Employee_Name: "Carney, Dank", Department: "Software Engineering", Position: "Software Engineer", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1013", Employee_Name: "Lujan, Tricia", Department: "Software Engineering", Position: "Software Engineer", EmploymentStatus: "Voluntarily Terminated", Sex: "F" },
            { EmpID: "1014", Employee_Name: "Warfield, Sarah", Department: "Software Engineering", Position: "Software Engineering Manager", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1015", Employee_Name: "Martin, Aaron", Department: "Software Engineering", Position: "Software Engineer", EmploymentStatus: "Future Start", Sex: "M" },

            // Sales
            { EmpID: "1016", Employee_Name: "Gonzales, Ricardo", Department: "Sales", Position: "Area Sales Manager", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1017", Employee_Name: "Akinkuolie, Sarah", Department: "Sales", Position: "Area Sales Manager", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1018", Employee_Name: "Sears, Rich", Department: "Sales", Position: "Sales Manager", EmploymentStatus: "Voluntarily Terminated", Sex: "M" },
            { EmpID: "1019", Employee_Name: "Ruiz, Ricardo", Department: "Sales", Position: "Area Sales Manager", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1020", Employee_Name: "Pratt, Thomas", Department: "Sales", Position: "Area Sales Manager", EmploymentStatus: "Terminated for Cause", Sex: "M" },
            { EmpID: "1021", Employee_Name: "Hansen, Joanne", Department: "Sales", Position: "Area Sales Manager", EmploymentStatus: "Leave of Absence", Sex: "F" },

            // Production (Largest Department)
            { EmpID: "1022", Employee_Name: "Albert, Dane", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1023", Employee_Name: "Bassi, Louisa", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1024", Employee_Name: "Candcer, Kim", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Voluntarily Terminated", Sex: "F" },
            { EmpID: "1025", Employee_Name: "Darling, Sarah", Department: "Production", Position: "Production Technician II", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1026", Employee_Name: "Eberhardt, Michael", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Terminated for Cause", Sex: "M" },
            { EmpID: "1027", Employee_Name: "Gentry, Ihor", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1028", Employee_Name: "Hakim, Valerie", Department: "Production", Position: "Production Technician II", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1029", Employee_Name: "Irons, Winfield", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Voluntarily Terminated", Sex: "M" },
            { EmpID: "1030", Employee_Name: "Jackson, Tara", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Leave of Absence", Sex: "F" },
            { EmpID: "1031", Employee_Name: "Kinsella, Kathleen", Department: "Production", Position: "Production Supervisor", EmploymentStatus: "Active", Sex: "F" },
            { EmpID: "1032", Employee_Name: "LeBlanc, Brandon", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Future Start", Sex: "M" },
            { EmpID: "1033", Employee_Name: "Miller, Derek", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1034", Employee_Name: "Norman, Eric", Department: "Production", Position: "Production Technician II", EmploymentStatus: "Voluntarily Terminated", Sex: "M" },
            { EmpID: "1035", Employee_Name: "O'Brien, Kevin", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Active", Sex: "M" },
            { EmpID: "1036", Employee_Name: "Peters, Lauren", Department: "Production", Position: "Production Technician I", EmploymentStatus: "Terminated for Cause", Sex: "F" }
        ];

        // Global State
        let rawData = [];
        let filteredData = [];
        let chartInstance = null;
        let currentSort = { column: 'EmpID', direction: 'asc' };

        document.addEventListener('DOMContentLoaded', () => {
            // Initialize Lucide Icons
            lucide.createIcons();

            // Load Default Data
            loadDataset(SAMPLE_HR_DATA, true);

            // Bind Event Listeners
            document.getElementById('file-input').addEventListener('change', handleFileUpload);
            document.getElementById('reset-data-btn').addEventListener('click', () => loadDataset(SAMPLE_HR_DATA, true));
            document.getElementById('filter-dept').addEventListener('change', applyFilters);
            document.getElementById('filter-status').addEventListener('change', applyFilters);
            document.getElementById('search-input').addEventListener('input', applyFilters);
            document.getElementById('clear-filters-btn').addEventListener('click', resetFilters);
        });

        // Load Dataset into Application
        function loadDataset(data, isSample = false) {
            rawData = data.map(item => ({
                EmpID: item.EmpID || item.Employee_ID || item.id || '-',
                Employee_Name: item.Employee_Name || item.EmpName || item.Name || 'ไม่ระบุชื่อ',
                Department: (item.Department || item.Dept || 'Unassigned').trim(),
                Position: item.Position || item.Title || '-',
                EmploymentStatus: (item.EmploymentStatus || item.Status || 'Active').trim(),
                Sex: item.Sex || item.Gender || '-'
            }));

            // Update Badge Status
            const badge = document.getElementById('data-source-badge');
            if (isSample) {
                badge.className = "px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200";
                badge.innerText = "ข้อมูลตัวอย่าง (Sample Data)";
            } else {
                badge.className = "px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 border border-indigo-200";
                badge.innerText = "ไฟล์อัปโหลดภายนอก (Custom Data)";
            }

            document.getElementById('total-rows-count').innerText = `${rawData.length} รายการ`;

            populateFilterDropdowns();
            resetFilters();
        }

        // File Upload Handler (Parses TSV or CSV)
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                const parsedData = parseDelimitedText(text);
                if (parsedData && parsedData.length > 0) {
                    loadDataset(parsedData, false);
                } else {
                    alert('ไม่สามารถอ่านไฟล์ได้ โปรดตรวจสอบว่าไฟล์เป็นรูปแบบ HR DATA.txt (TSV) หรือ CSV ที่ถูกต้อง');
                }
            };
            reader.readAsText(file);
        }

        // TSV / CSV Simple Parser
        function parseDelimitedText(text) {
            const lines = text.split(/\r\n|\n/).filter(line => line.trim() !== '');
            if (lines.length < 2) return [];

            // Detect Delimiter (Tab or Comma)
            const firstLine = lines[0];
            const delimiter = firstLine.includes('\t') ? '\t' : ',';

            const headers = firstLine.split(delimiter).map(h => h.trim().replace(/^["']|["']$/g, ''));
            const data = [];

            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(delimiter).map(v => v.trim().replace(/^["']|["']$/g, ''));
                if (values.length === headers.length) {
                    let row = {};
                    headers.forEach((header, index) => {
                        row[header] = values[index];
                    });
                    data.push(row);
                }
            }
            return data;
        }

        // Populate Dynamic Dropdown Filters
        function populateFilterDropdowns() {
            const deptSelect = document.getElementById('filter-dept');
            const statusSelect = document.getElementById('filter-status');

            const departments = [...new Set(rawData.map(d => d.Department))].sort();
            const statuses = [...new Set(rawData.map(d => d.EmploymentStatus))].sort();

            deptSelect.innerHTML = '<option value="ALL">-- ทุกแผนก (All Departments) --</option>';
            departments.forEach(dept => {
                deptSelect.innerHTML += `<option value="${dept}">${dept}</option>`;
            });

            statusSelect.innerHTML = '<option value="ALL">-- ทุกสถานะ (All Statuses) --</option>';
            statuses.forEach(status => {
                statusSelect.innerHTML += `<option value="${status}">${status}</option>`;
            });
        }

        // Reset All Filters
        function resetFilters() {
            document.getElementById('filter-dept').value = 'ALL';
            document.getElementById('filter-status').value = 'ALL';
            document.getElementById('search-input').value = '';
            applyFilters();
        }

        // Main Filter & Render Logic
        function applyFilters() {
            const selectedDept = document.getElementById('filter-dept').value;
            const selectedStatus = document.getElementById('filter-status').value;
            const searchQuery = document.getElementById('search-input').value.toLowerCase().trim();

            filteredData = rawData.filter(item => {
                const matchDept = (selectedDept === 'ALL' || item.Department === selectedDept);
                const matchStatus = (selectedStatus === 'ALL' || item.EmploymentStatus === selectedStatus);
                const matchSearch = searchQuery === '' || 
                    item.Employee_Name.toLowerCase().includes(searchQuery) ||
                    item.EmpID.toLowerCase().includes(searchQuery) ||
                    item.Department.toLowerCase().includes(searchQuery) ||
                    item.Position.toLowerCase().includes(searchQuery);

                return matchDept && matchStatus && matchSearch;
            });

            updateKPIs();
            renderChart();
            renderTable();
        }

        // Update KPI Dashboard Cards
        function updateKPIs() {
            const total = filteredData.length;
            const activeCount = filteredData.filter(d => d.EmploymentStatus === 'Active').length;
            const voluntaryCount = filteredData.filter(d => d.EmploymentStatus === 'Voluntarily Terminated').length;
            const causeCount = filteredData.filter(d => d.EmploymentStatus === 'Terminated for Cause').length;
            const otherCount = total - (activeCount + voluntaryCount + causeCount);

            const activePct = total > 0 ? ((activeCount / total) * 100).toFixed(1) : 0;
            const voluntaryPct = total > 0 ? ((voluntaryCount / total) * 100).toFixed(1) : 0;
            const causePct = total > 0 ? ((causeCount / total) * 100).toFixed(1) : 0;

            document.getElementById('kpi-total').innerText = total;
            document.getElementById('kpi-active').innerText = activeCount;
            document.getElementById('kpi-active-pct').innerText = `${activePct}% ของที่เลือก`;

            document.getElementById('kpi-voluntary').innerText = voluntaryCount;
            document.getElementById('kpi-voluntary-pct').innerText = `${voluntaryPct}% ของที่เลือก`;

            document.getElementById('kpi-cause').innerText = causeCount;
            document.getElementById('kpi-cause-pct').innerText = `${causePct}% ของที่เลือก`;

            document.getElementById('kpi-other').innerText = otherCount;
            document.getElementById('filtered-count-badge').innerText = `${total} รายการ`;
        }

        // Render Grouped Bar Chart (Employment Status by Department)
        function renderChart() {
            const ctx = document.getElementById('deptStatusChart').getContext('2d');

            // Unique Departments & Statuses from dataset
            const departments = [...new Set(filteredData.map(d => d.Department))].sort();
            const statuses = [...new Set(rawData.map(d => d.EmploymentStatus))].sort();

            // Prepare Chart.js Datasets
            const datasets = statuses.map(status => {
                const dataCounts = departments.map(dept => {
                    return filteredData.filter(d => d.Department === dept && d.EmploymentStatus === status).length;
                });

                const colorConfig = STATUS_COLORS[status] || DEFAULT_COLOR;

                return {
                    label: status,
                    data: dataCounts,
                    backgroundColor: colorConfig.bg,
                    borderColor: colorConfig.border,
                    borderWidth: 1,
                    borderRadius: 4,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7
                };
            });

            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: departments,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            align: 'end',
                            labels: {
                                font: { family: 'Sarabun', size: 11 },
                                usePointStyle: true,
                                boxWidth: 8
                            }
                        },
                        tooltip: {
                            callbacks: {
                                title: (items) => `แผนก: ${items[0].label}`,
                                label: (context) => ` ${context.dataset.label}: ${context.raw} คน`
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: {
                                font: { family: 'Sarabun', size: 11, weight: '500' },
                                color: '#475569'
                            }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                font: { family: 'Sarabun', size: 11 },
                                color: '#64748b'
                            },
                            title: {
                                display: true,
                                text: 'จำนวนพนักงาน (คน)',
                                font: { family: 'Sarabun', size: 11 }
                            }
                        }
                    }
                }
            });
        }

        // Render Employee Data Table
        function renderTable() {
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';

            if (filteredData.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="px-4 py-8 text-center text-slate-400">
                            ไม่พบข้อมูลตรงตามเงื่อนไข
                        </td>
                    </tr>
                `;
                document.getElementById('table-showing-info').innerText = 'แสดง 0 จาก 0 รายการ';
                return;
            }

            filteredData.forEach(emp => {
                const colorConfig = STATUS_COLORS[emp.EmploymentStatus] || DEFAULT_COLOR;
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50/80 transition border-b border-slate-100";
                tr.innerHTML = `
                    <td class="px-4 py-2.5 font-mono text-[11px] font-semibold text-indigo-900">${emp.EmpID}</td>
                    <td class="px-4 py-2.5 font-medium text-slate-800">${emp.Employee_Name}</td>
                    <td class="px-4 py-2.5 text-slate-600">${emp.Department}</td>
                    <td class="px-4 py-2.5 text-slate-600">${emp.Position}</td>
                    <td class="px-4 py-2.5">
                        <span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-semibold ${colorConfig.badge}">
                            ${emp.EmploymentStatus}
                        </span>
                    </td>
                    <td class="px-4 py-2.5 text-slate-500">${emp.Sex}</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('table-showing-info').innerText = `กำลังแสดงข้อมูล ${filteredData.length} จาก ${rawData.length} รายการ`;
        }

        // Table Sorting Logic
        function sortTable(column) {
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }

            filteredData.sort((a, b) => {
                let valA = a[column] || '';
                let valB = b[column] || '';

                if (!isNaN(valA) && !isNaN(valB)) {
                    valA = Number(valA);
                    valB = Number(valB);
                }

                if (valA < valB) return currentSort.direction === 'asc' ? -1 : 1;
                if (valA > valB) return currentSort.direction === 'asc' ? 1 : -1;
                return 0;
            });

            renderTable();
        }
    </script>
</body>
</html>