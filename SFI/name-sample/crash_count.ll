; ModuleID = 'crash_count.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-f128:128:128-n8:16:32:64"
target triple = "x86_64-unknown-linux-gnu"

%struct.FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct.FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct.FILE*, i32 }

@fi_cycle_counter = unnamed_addr global i64 0
@cycleInterval = unnamed_addr global i64 1
@cycleFactor = unnamed_addr global i64 1
@bbCounter = unnamed_addr global i64 0
@fiFlag = external unnamed_addr global i32
@.str = private unnamed_addr constant [23 x i8] c"crashcount_latency.txt\00", align 1
@.str1 = private unnamed_addr constant [2 x i8] c"w\00", align 1
@.str2 = private unnamed_addr constant [5 x i8] c"%lld\00", align 1

define void @latencyCount(i64 %llfiIndex) nounwind {
entry:
  %llfiIndex_addr = alloca i64, align 8
  %f = alloca %struct.FILE*
  %"alloca point" = bitcast i32 0 to i32
  store i64 %llfiIndex, i64* %llfiIndex_addr
  %0 = load i32* @fiFlag, align 4
  %1 = icmp eq i32 %0, 1
  br i1 %1, label %bb, label %bb4

bb:                                               ; preds = %entry
  %2 = load i64* @fi_cycle_counter, align 8
  %3 = add nsw i64 %2, 1
  store i64 %3, i64* @fi_cycle_counter, align 8
  %4 = load i64* @cycleInterval, align 8
  %5 = mul nsw i64 %4, 10
  %6 = load i64* @fi_cycle_counter, align 8
  %7 = icmp sle i64 %5, %6
  br i1 %7, label %bb1, label %bb2

bb1:                                              ; preds = %bb
  %8 = load i64* @cycleInterval, align 8
  %9 = mul nsw i64 %8, 10
  store i64 %9, i64* @cycleInterval, align 8
  store i64 1, i64* @cycleFactor, align 8
  br label %bb2

bb2:                                              ; preds = %bb1, %bb
  %10 = load i64* @cycleInterval, align 8
  %11 = load i64* @cycleFactor, align 8
  %12 = mul nsw i64 %10, %11
  %13 = load i64* @fi_cycle_counter, align 8
  %14 = icmp slt i64 %12, %13
  br i1 %14, label %bb3, label %bb4

bb3:                                              ; preds = %bb2
  %15 = load i64* @cycleFactor, align 8
  %16 = add nsw i64 %15, 1
  store i64 %16, i64* @cycleFactor, align 8
  %17 = call %struct.FILE* @fopen(i8* noalias getelementptr inbounds ([23 x i8]* @.str, i64 0, i64 0), i8* noalias getelementptr inbounds ([2 x i8]* @.str1, i64 0, i64 0)) nounwind
  store %struct.FILE* %17, %struct.FILE** %f, align 8
  %18 = load i64* @fi_cycle_counter, align 8
  %19 = load %struct.FILE** %f, align 8
  %20 = call i32 (%struct.FILE*, i8*, ...)* @fprintf(%struct.FILE* noalias %19, i8* noalias getelementptr inbounds ([5 x i8]* @.str2, i64 0, i64 0), i64 %18) nounwind
  %21 = load %struct.FILE** %f, align 8
  %22 = call i32 @fclose(%struct.FILE* %21) nounwind
  br label %bb4

bb4:                                              ; preds = %bb3, %bb2, %entry
  br label %return

return:                                           ; preds = %bb4
  ret void
}

declare %struct.FILE* @fopen(i8* noalias, i8* noalias)

declare i32 @fprintf(%struct.FILE* noalias, i8* noalias, ...) nounwind

declare i32 @fclose(%struct.FILE*)
