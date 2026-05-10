// composables/use-model-inference.ts
//
// Loads the XGBoost ONNX model and runs client-side inference to produce
// a password strength score (0–100). The ONNX session is created once and
// cached for the lifetime of the page — subsequent calls reuse the same
// session without reloading the model file.
//
// Usage:
//   const { predictStrength, loadModel, isLoading, error } = useModelInference()
//   onMounted(() => loadModel())
//   const score = await predictStrength(featureVector)

import { ref } from "vue";
import * as ort from "onnxruntime-web";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MODEL_PATH = "/model/password-model.onnx";
const ORT_WASM_PATH = "/ort/";
const FEATURE_COUNT = 16;
const SCORE_MIN = 0;
const SCORE_MAX = 100;

// ---------------------------------------------------------------------------
// Session cache — lives outside the composable so it is shared across all
// instances and the model is only loaded once per page lifetime.
// ---------------------------------------------------------------------------

let sessionPromise: Promise<ort.InferenceSession> | null = null;

const getSession = async (): Promise<ort.InferenceSession> => {
  if (!sessionPromise) {
    ort.env.wasm.wasmPaths = ORT_WASM_PATH;
    sessionPromise = ort.InferenceSession.create(MODEL_PATH);
  }
  return sessionPromise;
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const clamp = (value: number, min: number, max: number): number =>
  Math.min(max, Math.max(min, value));

const toErrorMessage = (caught: unknown, fallback: string): string =>
  caught instanceof Error ? caught.message : fallback;

// ---------------------------------------------------------------------------
// Composable
// ---------------------------------------------------------------------------

export const useModelInference = () => {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Pre-warm the ONNX session on page mount so the model is ready before
   * the user types. Call this from onMounted() in the parent component.
   */
  const loadModel = async (): Promise<void> => {
    isLoading.value = true;
    error.value = null;

    try {
      await getSession();
    } catch (caught) {
      error.value = toErrorMessage(
        caught,
        "Failed to load the strength model.",
      );
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Run inference on a feature vector and return a strength score 0–100.
   *
   * @param features - Flat numeric array of exactly 16 features in this order:
   *   [length, entropyBits, hasUppercase, hasLowercase, hasDigits,
   *    hasSpecialChars, uniqueCharRatio, charClassCount, zxcvbnScore,
   *    zxcvbnGuessesLog10, hasDictionaryMatch, hasL33tSub,
   *    hasKeyboardPattern, hasDatePattern, hasRepeat, hasSequence]
   *
   * Returns 0 on validation failure or inference error.
   */
  const predictStrength = async (features: number[]): Promise<number> => {
    // --- input validation --------------------------------------------------
    if (features.length !== FEATURE_COUNT) {
      error.value = `Expected ${FEATURE_COUNT} features, got ${features.length}.`;
      return 0;
    }

    if (features.some((f) => !Number.isFinite(f))) {
      error.value =
        "Feature vector contains non-finite values (NaN or Infinity).";
      return 0;
    }

    // --- inference ---------------------------------------------------------
    isLoading.value = true;
    error.value = null;

    try {
      const session = await getSession();
      const inputName = session.inputNames[0];
      const outputName = session.outputNames[0];

      const tensor = new ort.Tensor("float32", Float32Array.from(features), [
        1,
        FEATURE_COUNT,
      ]);

      const outputs = await session.run({ [inputName]: tensor });
      const result = outputs[outputName];
      const outputArray = result.data as Float32Array | number[];
      const rawScore = Number(outputArray[0] ?? 0);

      return Math.round(clamp(rawScore, SCORE_MIN, SCORE_MAX));
    } catch (caught) {
      error.value = toErrorMessage(
        caught,
        "Model inference failed unexpectedly.",
      );
      return 0;
    } finally {
      isLoading.value = false;
    }
  };

  // -------------------------------------------------------------------------

  return {
    isLoading,
    error,
    loadModel,
    predictStrength,
  };
};
