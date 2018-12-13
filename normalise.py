#Note the Scala one is in npfl

import os, sys

ffmpeg = r"F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin\ffmpeg.exe"
print(ffmpeg)

def remove(files, f):
    if f in files: files.remove(f)

def normalise(fin, fout):
    cmd = ffmpeg + " -hwaccel nvdec -i %s -filter:a loudnorm -c:v h264_nvenc %s"
    run = cmd % (fin, fout)
    print(run)
    os.system(run)

def slice_vids(files, slices):
    cmd = ffmpeg + " -i %s -vcodec copy -acodec copy -ss %s -t %s %s"
    for (f, (start, end)) in slices.items():
        remove(files, f)
        files.append(f + "-sliced")
        run = cmd % (f + ".mp4", start, end, f + "-sliced.mp4")
        #print(run)
        os.system(run)

def concat_vids(files, concats):
    cmd1 = ffmpeg + " -hwaccel nvdec -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-1.ts"
    cmd2 = ffmpeg + " -hwaccel nvdec -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-2.ts"
    cmd3 = ffmpeg + " -hwaccel nvdec -f mpegts -i \"concat:tmp-1.ts|tmp-2.ts\" -c copy -bsf:a aac_adtstoasc %s"
    cmd4 = "del tmp-1.ts tmp-2.ts"
    for ((s, e), to) in concats:
        remove(files, s)
        remove(files, e)
        files.append(to)
        #concat the files
        os.system(cmd1 % (s + ".mp4"))
        os.system(cmd2 % (e + ".mp4"))
        os.system(cmd3 % (to + ".mp4"))
        os.system(cmd4)

def rm_vids(files, rms):
    for f in rms:
        remove(files, f)
        os.system("del " + f + ".mp4")

dirs = [d for d in os.listdir(".") if os.path.isdir(d)]
#print(dirs)

files = [os.path.join(d, f)[:-4] for d in dirs for f in os.listdir(d)]

slices = {
    "Erlang\\MVI_0014" : ("00:00:26", "00:34:26"),
    "Erlang\\MVI_0021" : ("00:00:30", "00:31:20"),
    "Haskell2\\MVI_0009" : ("00:00:00", "00:00:16"),
    "ML\\MVI_0004" : ("00:00:36", "00:24:06"),
    "ML\\MVI_0005" : ("00:00:48", "00:21:42"),
    "npfl\\MVI_0013" : ("00:01:37", "00:34:29"),
    "Scala\\MVI_0417" : ("00:06:25", "00:33:25"),
    "Scala\\MVI_0425" : ("00:00:30", "00:22:52")
}

slice_vids(files, slices)

concats = [
    (("Erlang\\MVI_0014-sliced", "Erlang\\MVI_0015"), "Erlang\\MVI_0014-5"),
    (("Erlang\\MVI_0014-5", "Erlang\\MVI_0016"), "Erlang\\MVI_0014-16"),
    (("FHPC\\MVI_0433", "FHPC\\MVI_0434"), "FHPC\\MVI_0433-4"),
    (("FHPC\\MVI_0435", "FHPC\\MVI_0436"), "FHPC\\MVI_0435-6"),
    (("FHPC\\MVI_0437", "FHPC\\MVI_0438"), "FHPC\\MVI_0437-8"),
    (("FHPC\\MVI_0439", "FHPC\\MVI_0440"), "FHPC\\MVI_0439-40"),
    (("FHPC\\MVI_0441", "FHPC\\MVI_0442"), "FHPC\\MVI_0441-2"),
    (("FHPC\\MVI_0443", "FHPC\\MVI_0444"), "FHPC\\MVI_0443-4"),
    (("Haskell2\\MVI_0008", "Haskell2\\MVI_0009-sliced"), "Haskell2\\MVI_0008-9"),
    (("ML\\MVI_0001", "ML\\MVI_0002"), "ML\\MVI_0001-2"),
    (("ML\\MVI_0011", "ML\\MVI_0012"), "ML\\MVI_0011-2"),
    (("npfl\\MVI_0013-sliced", "npfl\\MVI_0014"), "npfl\\MVI_0013-4"),
    (("npfl\\MVI_0016", "npfl\\MVI_0017"), "npfl\\MVI_0016-7"),
    (("npfl\\MVI_0018", "npfl\\MVI_0019"), "npfl\\MVI_0018-9"),
    (("npfl\\MVI_0022", "npfl\\MVI_0023"), "npfl\\MVI_0022-3"),
    (("Scala\\MVI_0417-sliced", "Scala\\MVI_0418"), "Scala\\MVI_0417-8")
]

concat_vids(files, concats)

rms = ["Erlang\\MVI_0014-sliced", "Erlang\\MVI_0014-5", "Haskell2\\MVI_0009-sliced", "npfl\\MVI_0013-sliced", "Scala\\MVI_0417-sliced"]

rm_vids(files, rms)

outmap = {
    "Erlang\\MVI_0013" : "Erlang\\Junk",
    "Erlang\\MVI_0014-16" : "Erlang\\DistErlangDataToPlanet",
    "Erlang\\MVI_0017" : "Erlang\\Updates",
    "Erlang\\MVI_0018" : "Erlang\\UnderstandingFormalSpecs",
    "Erlang\\MVI_0019" : "Erlang\\TowardsSecureErlangSystems",
    "Erlang\\MVI_0020" : "Erlang\\AnImmersiveDebuggerForActors",
    "Erlang\\MVI_0021-sliced" : "Erlang\\AutomaticDetectionOfCoreErlangMessagePassingErrors",
    "Erlang\\MVI_0022" : "Erlang\\ModellingDistributedErlangWithinASingleNode",
    "Erlang\\MVI_0023" : "Erlang\\ModelingErlangProcessesAsPetriNets",
    "Erlang\\MVI_0024" : "Erlang\\TypingTheWildInErlang",
    "Erlang\\MVI_0025" : "Erlang\\Outro",
    "Haskell2\\MVI_0001" : "Haskell2\\DerivingVia",
    "Haskell2\\MVI_0002" : "Haskell2\\GenericProgrammingOfAllKinds",
    "Haskell2\\MVI_0003" : "Haskell2\\TypeVariablesInPatterns",
    "Haskell2\\MVI_0004" : "Haskell2\\TheThoralfPlugin",
    "Haskell2\\MVI_0005" : "Haskell2\\SuggestingValidHoleFitsForTypedHoles",
    "Haskell2\\MVI_0006" : "Haskell2\\APromiseCheckedIsAPromiseKept",
    "Haskell2\\MVI_0007" : "Haskell2\\BranchingProcessesForQuickcheckGenerators",
    "Haskell2\\MVI_0008-9" : "Haskell2\\CoherentExplicitDictionaryApplication",
    "Haskell2\\MVI_0010" : "Haskell2\\TheoremProvingForAll",
    "ML\\MVI_0001-2" : "ML\\ElpiAnExtensionLanguageWithBindersAndUnificationVariables",
    "ML\\MVI_0003" : "ML\\SafelyMixingOCamlAndRust",
    "ML\\MVI_0004-sliced" : "ML\\RustDistilledAnExpressiveTowerOfLanguages",
    "ML\\MVI_0005-sliced" : "ML\\GeneratingMutuallyRecursiveDefinitions",
    "ML\\MVI_0006" : "ML\\TypeSafeMultiTierProgrammingWithStandardMLModules",
    "ML\\MVI_0007" : "ML\\MLAsATacticLanguageAgain",
    "ML\\MVI_0008" : "ML\\DesignAndVerificationOfFunctionalProofCheckers",
    "ML\\MVI_0009" : "ML\\Disornamentation",
    "ML\\MVI_0010" : "ML\\GenericProgrammingWithCombinatorsAndObjects",
    "ML\\MVI_0011-2" : "ML\\ProgrammingWithAbstractAlgebraicEffects",
    "npfl\\MVI_0013-4" : "npfl\\Daisy",
    "npfl\\MVI_0015" : "npfl\\Hasktorch",
    "npfl\\MVI_0016-7" : "npfl\\APLicativeProgrammingWithNaperianFunctors",
    "npfl\\MVI_0018-9" : "npfl\\ErrorAnalysisAlmostForFree",
    "npfl\\MVI_0020" : "npfl\\AHaskellInterfaceToSundialsViaInlineC",
    "npfl\\MVI_0021" : "npfl\\NumericalProgrammingInFunctionalLanguages2018",
    "npfl\\MVI_0022-3" : "npfl\\ManifoldsAsHaskellTypes",
    "npfl\\MVI_0024" : "npfl\\Junk",
    "npfl\\MVI_0025" : "npfl\\ExactRealArithmeticForGeometricComputation",
    "Scala\\MVI_0417-8" : "Scala\\CrossPlatformLanguageDesignInScalaJs",
    "Scala\\MVI_0419" : "Scala\\ExtendingScalaWithRecords",
    "Scala\\MVI_0420" : "Scala\\TowardsSafeIninitializationForScala",
    "Scala\\MVI_0421" : "Scala\\PathDependentTypesWithPathEquality",
    "Scala\\MVI_0422" : "Scala\\KDOTScalingDOTWithMutationAndConstructors",
    "Scala\\MVI_0423" : "Scala\\JuliaLessonsScalaCouldLearn",
    "Scala\\MVI_0424" : "Scala\\ScalaWithExplicitNull",
    "Scala\\MVI_0425-sliced" : "Scala\\GarnishingParsecWithParsley",
    "Scala\\MVI_0426" : "Scala\\Interflow",
    "Scala\\MVI_0427" : "Scala\\ParserCombinatorForContextFreePathQuerying",
    "Scala\\MVI_0428" : "Scala\\TrulyAbstractInterfacesForAlgebraicDataTypes",
    "Scala\\MVI_0429" : "Scala\\AddingPolymorphicFunctionsToScala",
    "Scala\\MVI_0430" : "Scala\\ValidatingChangesInTypeCheckingOnCodebases",
    "Scala\\MVI_0431" : "Scala\\ADomainSpecificLanguageForMicroservices",
    "Scala\\MVI_0432" : "Scala\\SemanticDBACommonDataModelForScalaDeveloperTools"
}

for f in files:
    fin = f + ".mp4"
    fout = outmap[f] + ".mp4" if f in outmap else f + "normhw.mp4"
    print("normalising " + fin + " to " + fout)
    normalise(fin, fout)
