; ModuleID = 'smartProfile.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-f128:128:128-n8:16:32:64"
target triple = "x86_64-unknown-linux-gnu"

%struct.FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct.FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct.FILE*, i32 }

@instructionCounter = unnamed_addr global i64 0
@currentCallSeq = unnamed_addr global i64 1
@callSeqSize = unnamed_addr global i64 0
@currentFunctionIndex = unnamed_addr global i32 -1
@targetFunctionIndex = unnamed_addr global i32 -1
@targetLlfiIndex = unnamed_addr global i64 1347
@callSeqList = common unnamed_addr global [1000000 x i64] zeroinitializer, align 32
@.str = private unnamed_addr constant [17 x i8] c"CFD_fi_cycle.txt\00", align 1
@.str1 = private unnamed_addr constant [2 x i8] c"a\00", align 1
@.str2 = private unnamed_addr constant [6 x i8] c"%lld\0A\00", align 1

define void @functionCall(i32 %functionIndex) nounwind {
entry:
  %functionIndex_addr = alloca i32, align 4
  %"alloca point" = bitcast i32 0 to i32
  store i32 %functionIndex, i32* %functionIndex_addr
  %0 = load i32* %functionIndex_addr, align 4
  store i32 %0, i32* @currentFunctionIndex, align 4
  %1 = load i32* %functionIndex_addr, align 4
  %2 = sext i32 %1 to i64
  %3 = load i64* @currentCallSeq, align 8
  %4 = add nsw i64 %2, %3
  %5 = load i32* %functionIndex_addr, align 4
  %6 = sext i32 %5 to i64
  %7 = mul nsw i64 %4, %6
  %8 = load i32* %functionIndex_addr, align 4
  %9 = add nsw i32 %8, 1
  %10 = sext i32 %9 to i64
  %11 = sdiv i64 %7, %10
  store i64 %11, i64* @currentCallSeq, align 8
  br label %return

return:                                           ; preds = %entry
  ret void
}

define void @instructionCall(i64 %llfiIndex) nounwind {
entry:
  %llfiIndex_addr = alloca i64, align 8
  %i = alloca i32
  %f = alloca %struct.FILE*
  %"alloca point" = bitcast i32 0 to i32
  store i64 %llfiIndex, i64* %llfiIndex_addr
  %0 = load i64* @targetLlfiIndex, align 8
  %1 = load i64* %llfiIndex_addr, align 8
  %2 = icmp eq i64 %1, %0
  br i1 %2, label %bb, label %bb2

bb:                                               ; preds = %entry
  %3 = load i32* @targetFunctionIndex, align 4
  %4 = icmp eq i32 %3, -1
  br i1 %4, label %bb1, label %bb2

bb1:                                              ; preds = %bb
  %5 = load i32* @currentFunctionIndex, align 4
  store i32 %5, i32* @targetFunctionIndex, align 4
  br label %bb2

bb2:                                              ; preds = %bb1, %bb, %entry
  %6 = load i64* @instructionCounter, align 8
  %7 = add nsw i64 %6, 1
  store i64 %7, i64* @instructionCounter, align 8
  %8 = load i64* @targetLlfiIndex, align 8
  %9 = load i64* %llfiIndex_addr, align 8
  %10 = icmp eq i64 %9, %8
  br i1 %10, label %bb3, label %bb9

bb3:                                              ; preds = %bb2
  store i32 0, i32* %i, align 4
  br label %bb7

bb4:                                              ; preds = %bb7
  %11 = load i32* %i, align 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds [1000000 x i64]* @callSeqList, i64 0, i64 %12
  %14 = load i64* %13, align 8
  %15 = load i64* @currentCallSeq, align 8
  %16 = icmp eq i64 %14, %15
  br i1 %16, label %bb5, label %bb6

bb5:                                              ; preds = %bb4
  store i64 1, i64* @currentCallSeq, align 8
  br label %bb9

bb6:                                              ; preds = %bb4
  %17 = load i32* %i, align 4
  %18 = add nsw i32 %17, 1
  store i32 %18, i32* %i, align 4
  br label %bb7

bb7:                                              ; preds = %bb6, %bb3
  %19 = load i32* %i, align 4
  %20 = sext i32 %19 to i64
  %21 = load i64* @callSeqSize, align 8
  %22 = icmp slt i64 %20, %21
  br i1 %22, label %bb4, label %bb8

bb8:                                              ; preds = %bb7
  %23 = load i64* @callSeqSize, align 8
  %24 = load i64* @currentCallSeq, align 8
  %25 = getelementptr inbounds [1000000 x i64]* @callSeqList, i64 0, i64 %23
  store i64 %24, i64* %25, align 8
  %26 = load i64* @callSeqSize, align 8
  %27 = add nsw i64 %26, 1
  store i64 %27, i64* @callSeqSize, align 8
  store i64 1, i64* @currentCallSeq, align 8
  %28 = call %struct.FILE* @fopen(i8* noalias getelementptr inbounds ([17 x i8]* @.str, i64 0, i64 0), i8* noalias getelementptr inbounds ([2 x i8]* @.str1, i64 0, i64 0)) nounwind
  store %struct.FILE* %28, %struct.FILE** %f, align 8
  %29 = load i64* @instructionCounter, align 8
  %30 = load %struct.FILE** %f, align 8
  %31 = call i32 (%struct.FILE*, i8*, ...)* @fprintf(%struct.FILE* noalias %30, i8* noalias getelementptr inbounds ([6 x i8]* @.str2, i64 0, i64 0), i64 %29) nounwind
  %32 = load %struct.FILE** %f, align 8
  %33 = call i32 @fclose(%struct.FILE* %32) nounwind
  br label %bb9

bb9:                                              ; preds = %bb8, %bb5, %bb2
  br label %return

return:                                           ; preds = %bb9
  ret void
}

declare %struct.FILE* @fopen(i8* noalias, i8* noalias)

declare i32 @fprintf(%struct.FILE* noalias, i8* noalias, ...) nounwind

declare i32 @fclose(%struct.FILE*)
