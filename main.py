from src.hybrid_system import HybridExpertSystem

def main():
    system = HybridExpertSystem()
    test_cases = [
        [],
        ["fievre", "toux", "fatigue"],
        ["eternuement", "yeux_rouges"],
        ["fievre_elevee", "yeux_rouges"]
    ]

    print("--- EXECUTION DES CAS DE TEST ---")
    for i, symptoms in enumerate(test_cases, 1):
        res = system.diagnose(symptoms)
        print(f"\nCas {i} {symptoms}:")
        print(f"  Diagnostic : {res['diagnostic']} (Confiance: {res['confiance']*100:.1f}%)")
        print(f"  Raisonnement: {res['explication']}")

if __name__ == "__main__":
    main()