#!/usr/bin/env bash
# collect_hardware.sh
# 采集 macOS 本机硬件配置信息，输出结构化文本，供后续打分使用
# 用法: bash collect_hardware.sh

set -euo pipefail

echo "====== 硬件信息采集报告 ======"
echo "采集时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ---------- 机型 ----------
echo "--- 机型 ---"
system_profiler SPHardwareDataType 2>/dev/null | grep -E \
  "Model Name|Model Identifier|Chip|Processor Name|Processor Speed|Number of Processors|Total Number of Cores|Hyper-Threading|Memory:|Serial Number" \
  | sed 's/^[[:space:]]*//'

echo ""

# ---------- CPU ----------
echo "--- CPU 详情 ---"
sysctl -n machdep.cpu.brand_string 2>/dev/null && echo "CPU型号: $(sysctl -n machdep.cpu.brand_string)"
echo "物理核心数: $(sysctl -n hw.physicalcpu 2>/dev/null || echo N/A)"
echo "逻辑核心数: $(sysctl -n hw.logicalcpu 2>/dev/null || echo N/A)"
echo "CPU频率: $(sysctl -n hw.cpufrequency_max 2>/dev/null | awk '{printf "%.2f GHz\n", $1/1e9}' 2>/dev/null || echo N/A)"

echo ""

# ---------- 内存 ----------
echo "--- 内存 ---"
echo "总内存: $(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.0f GB\n", $1/1073741824}' || echo N/A)"
system_profiler SPMemoryDataType 2>/dev/null | grep -E "Size:|Speed:|Type:|Manufacturer:|Status:" \
  | head -20 | sed 's/^[[:space:]]*//'

echo ""

# ---------- 存储 ----------
echo "--- 存储 ---"
system_profiler SPStorageDataType 2>/dev/null | grep -E \
  "Medium Type|Protocol|Total Capacity|S.M.A.R.T. Status|Device Name|BSD Name" \
  | sed 's/^[[:space:]]*//'
df -h / 2>/dev/null | tail -1 | awk '{print "根分区: 总量="$2, "已用="$3, "可用="$4}'

echo ""

# ---------- 显卡 ----------
echo "--- 显卡 ---"
system_profiler SPDisplaysDataType 2>/dev/null | grep -E \
  "Chipset Model|Type|VRAM|Vendor|Bus|Resolution|Display Type" \
  | sed 's/^[[:space:]]*//'

echo ""

# ---------- 屏幕 ----------
echo "--- 屏幕分辨率 ---"
system_profiler SPDisplaysDataType 2>/dev/null | grep -E "Resolution:|Retina:" \
  | sed 's/^[[:space:]]*//'

echo ""

# ---------- 网络 ----------
echo "--- 网络接口 ---"
networksetup -listallhardwareports 2>/dev/null | grep -E "Hardware Port|Ethernet Address" \
  | sed 's/^[[:space:]]*//'

echo ""

# ---------- 电池（笔记本） ----------
echo "--- 电池 ---"
system_profiler SPPowerDataType 2>/dev/null | grep -E \
  "Cycle Count|Condition|Maximum Capacity|Full Charge Capacity|Amperage" \
  | sed 's/^[[:space:]]*//'

echo ""
echo "====== 采集完毕 ======"
