정의부터.

중요한 연구란, 한 커뮤니티가 “무엇을 문제로 봐야 하는지, 무엇이 가능해졌는지, 무엇을 측정·설계·제작해야 하는지”를 바꾸는 연구다.
단순히 새롭거나 어려운 것이 아니라, 중심 병목을 건드리고, 신뢰 가능한 증거를 만들며, 다른 사람들이 재사용할 수 있는 개념·방법·시스템·데이터·프레임을 남기는 연구다.

이 정의는 Stokes의 use-inspired basic research, Hamming의 “중요한 문제이면서도 공격 가능한 문제를 잡아야 한다”는 원칙, NSF의 intellectual merit/broader impacts, CHI/SIGGRAPH의 contribution·significance·validity 기준을 합친 실전적 정의에 가깝다.

⸻

1. 중요한 연구의 핵심 조건

1) 문제 자체가 커야 한다

좋은 연구는 “내가 풀 수 있는 문제”에서 시작하면 약하다. 먼저 커뮤니티가 반복해서 우회하고 있는 병목을 찾아야 한다. Hamming은 중요한 연구를 하려면 중요한 문제를 붙잡되, 완전히 손댈 수 없는 문제가 아니라 “reasonable attack”이 가능한 문제를 잡아야 한다고 말한다.

문제 정의는 다음 형태가 가장 강하다.

현재 분야는 A를 하고 싶지만, B라는 가정/기술/제작/평가 병목 때문에 C 이상으로 가지 못한다.
우리는 이 병목을 D라는 새로운 관점/방법/시스템으로 바꾸고, 그 결과 E라는 새로운 연구·제작·사용 가능성을 연다.

이 구조가 없으면 연구는 “흥미로운 데모”에 머문다.

⸻

2) 기초성과 사용성이 동시에 있어야 한다

Stokes의 Pasteur’s Quadrant가 중요한 이유는, 좋은 연구가 꼭 “순수 이론”이거나 “응용 개발” 중 하나일 필요가 없다는 점이다. 강한 연구는 근본적 이해를 밀어붙이면서도 실제 필요에서 출발할 수 있다.

Graphics/HCI/Robotics에서는 특히 이게 중요하다. 좋은 주제는 “쓸모 있는 툴”이 아니라, 그 툴을 통해 새로운 표현, 새로운 제작 가능성, 새로운 상호작용 모델, 새로운 계산 문제를 드러내야 한다.

예를 들어:

* 나쁜 framing: “LLM으로 automata design을 도와주는 툴”
* 강한 framing: “비전문가가 motion intent를 물리적 mechanism space로 변환할 때 생기는 under-constrained design problem을 어떻게 표현·탐색·검증할 것인가”

두 번째는 도구를 넘어서 문제 공간을 정의한다.

⸻

3) contribution type이 명확해야 한다

HCI 문헌에서는 contribution을 empirical, artifact, methodological, theoretical, benchmark/dataset, survey, opinion 등으로 나누어 설명한다. 즉, “시스템을 만들었다” 자체는 contribution이 아니다. 시스템이 어떤 지식 단위를 생산하는지가 contribution이다.

Graphics/SIGGRAPH 쪽에서도 핵심은 유사하다. 논문은 novel하고, 잘 검증되어야 하며, state of the art를 실제로 전진시켜야 한다.

따라서 연구를 시작할 때 먼저 정해야 한다.

Contribution	질문
Method	이전에는 불가능했던 계산/최적화/표현을 가능하게 하는가?
System / Artifact	시스템이 단순 구현물이 아니라 새로운 design space를 드러내는가?
Empirical	사람들이 어떻게 생각·제작·실패하는지에 대한 일반화 가능한 사실을 주는가?
Theory / Framework	분야가 문제를 보는 언어를 바꾸는가?
Dataset / Benchmark	이후 연구가 비교·측정할 기준을 제공하는가?
Design knowledge	특정 도메인의 설계 원리를 재사용 가능하게 정리하는가?

중요한 연구는 보통 이 중 하나가 아니라, 주 contribution 하나 + 보조 contribution 하나를 가진다. 예: method + system, artifact + empirical study, framework + benchmark.

⸻

2. 임팩트 있는 연구의 구조

나는 다음 공식이 가장 실전적이라고 본다.

Research Impact = Problem Centrality × New Insight × Evidence Quality × Reusability × Timing × Framing

하나라도 0이면 약해진다.

Problem Centrality

Heilmeier Catechism은 DARPA식 문제정의 프레임으로 유용하다. 핵심 질문은 “무엇을 하려는가?”, “현재는 어떻게 하고 있으며 한계는 무엇인가?”, “무엇이 새롭고 왜 성공할 것인가?”, “누가 신경 쓰며 성공하면 무엇이 달라지는가?”, “위험은 무엇인가?”, “검증 기준은 무엇인가?”이다.

이 질문에 답하지 못하는 연구는 대개 아직 주제가 아니다. 그냥 아이디어다.

New Insight

새로움은 “처음 했다”가 아니다. 중요한 새로움은 기존의 강한 가정 하나를 바꾸는 것이다. Davis의 고전적 논의에서도 흥미로운 연구는 독자가 당연하다고 믿던 가정을 흔들 때 생긴다고 설명한다.

Graphics/HCI에서는 다음이 강한 insight가 된다.

* “정확한 motion reproduction보다 semantic motion equivalence가 fabrication에 더 중요하다.”
* “캐릭터 제작에서 geometry segmentation보다 actuation-aware part semantics가 더 근본 병목이다.”
* “novice creativity의 병목은 CAD skill이 아니라 mechanism search space를 mental model로 잡지 못하는 데 있다.”
* “2D로 줄이는 것은 단순 simplification이 아니라 fabrication-constrained motion retargeting이다.”

이런 문장은 연구의 뼈대가 된다.

Evidence Quality

CHI는 significance, originality, validity, clarity, related work를 주요 기준으로 보고, contribution과 significance를 특히 중요하게 본다.
NeurIPS도 reproducibility, transparency, ethics, societal impact를 체크리스트로 강제한다. 즉, 현대 연구에서 “작동함”만으로는 부족하고, 주장과 증거의 대응이 중요하다.

좋은 evidence는 claim에 맞아야 한다.

Claim	필요한 증거
더 정확하다	benchmark, ablation, statistical comparison
더 제작 가능하다	fabrication trials, failure analysis, tolerance study
더 창의적 탐색을 돕는다	user study, design process analysis, qualitative coding
더 일반적이다	multiple domains, boundary cases, stress tests
새로운 문제정의다	taxonomy, case analysis, counterexamples, design space mapping
시스템 기여다	end-to-end examples, expert feedback, reproducibility package

HCI/Design 연구에서는 특히 “평가”를 단일 잣대로 보면 안 된다. Research through Design와 design science 문헌은 artifact를 만드는 행위 자체가 지식 생산이 될 수 있지만, 그 지식이 무엇인지 명확히 해야 한다고 본다.

Reusability

Hamming은 좋은 연구가 특정 문제 하나를 푸는 데 그치지 않고, 사람들이 그 위에 쌓아 올릴 수 있어야 한다고 강조한다.

따라서 연구 결과물은 최소 하나를 남겨야 한다.

* reusable formulation
* algorithm
* design space
* benchmark
* dataset
* toolkit
* taxonomy
* evaluation protocol
* fabrication pipeline
* theory of failure modes
* open-source implementation

“내 시스템으로 이런 예제를 만들었다”는 약하다.
“이 유형의 문제를 앞으로 이렇게 표현하고 비교할 수 있다”가 강하다.

Timing

대규모 science-of-science 연구들은 임팩트가 순수 novelty만으로 생기지 않는다는 점을 보여준다. 높은 영향력의 연구는 보통 익숙한 지식 구조 위에 비전형적 조합을 주입한다. 즉, 완전히 외계적인 연구보다 커뮤니티가 이해할 수 있는 문법 안에서 한 지점을 비트는 연구가 더 강하다.

또 다른 연구는 작은 팀이 더 disruptive한 아이디어를 내는 경향이 있고, 큰 팀은 기존 흐름을 발전시키는 경향이 있음을 보였다. 둘 다 필요하지만, PhD 연구자가 노릴 수 있는 것은 보통 작은 팀형 disruption이다.

⸻

3. 접근법: 좋은 연구 주제를 만드는 절차

Step 1. 분야의 “반복 실패”를 찾는다

논문을 읽을 때 novelty만 보지 말고, 모두가 피해 가는 부분을 봐야 한다.

찾아야 할 문장들:

* “we assume…”
* “we leave fabrication to future work…”
* “our system requires expert tuning…”
* “we only demonstrate on simple examples…”
* “physical validation remains challenging…”
* “semantic intent is difficult to evaluate…”
* “users still need to manually…”

이런 문장이 연구 주제의 광맥이다.

⸻

Step 2. 문제를 “현상”이 아니라 “병목”으로 쓴다

약한 문제정의:

3D character를 cable-driven robot으로 만들고 싶다.

강한 문제정의:

3D character mesh를 cable-driven articulated artifact로 변환하려면 geometry segmentation, joint placement, tendon routing, material compliance, target motion이 서로 얽힌다. 기존 방법은 이들을 독립 단계로 다루기 때문에, visually meaningful motion과 fabricatable actuation을 동시에 보장하지 못한다.

이 정도로 써야 연구 문제가 된다.

⸻

Step 3. 해결책보다 “표현”을 먼저 만든다

중요한 연구는 대개 solver보다 representation이 먼저다.

Graphics/HCI/Robotics에서 강한 연구는 보통 다음 중 하나를 새로 정의한다.

* motion intent representation
* fabrication-aware kinematic representation
* actuation-constrained character abstraction
* semantic equivalence metric
* design-space grammar
* failure-mode taxonomy
* differentiable objective
* interactive exploration model
* benchmark task family

좋은 representation은 후속 연구를 만든다. 단순 pipeline은 후속 연구를 잘 못 만든다.

⸻

Step 4. claim을 작게 만들지 말고, 증거를 정확히 맞춘다

큰 연구는 claim이 크지만, 허풍이 아니다. claim을 명확히 제한한다.

예:

우리는 모든 캐릭터를 로봇으로 만든다.
→ 약함. 과장.

우리는 freeform character mesh에서 visually salient limb motion을 cable-driven planar actuation으로 변환하는 첫 fabrication-aware formulation을 제시한다.
→ 강함. 범위가 있지만 contribution이 선명함.

⸻

Step 5. 논문이 아니라 “field object”를 만든다

주요하게 다뤄지는 연구는 논문 안에 갇히지 않는다. 사람들이 계속 부를 수 있는 object를 만든다.

예:

* “motion graph”
* “motion matching”
* “Gaussian splatting”
* “NeRF”
* “design probes”
* “end-user programming”
* “computational design”
* “Pasteur’s Quadrant”
* “wicked problems”

Rittel과 Webber의 wicked problems처럼, 좋은 개념은 복잡한 문제군을 이름 붙여서 분야가 다시 말하게 만든다.

연구 제목과 framing은 그래서 중요하다. 좋은 연구는 “우리가 만든 시스템”보다 “이제 이 문제를 이렇게 불러야 한다”에 가깝다.

⸻

4. “주요하게 다뤄지는” 연구의 조건

연구가 major하게 다뤄지려면 다음 네 가지가 필요하다.

1) 커뮤니티 중심부와 연결되어야 한다

아무리 좋은 아이디어라도, 해당 venue의 중심 관심사와 연결되지 않으면 minor로 읽힌다. CHI는 HCI에 대한 명확한 contribution을 요구하고, SIGGRAPH는 visual computing 전반에서 scientific excellence와 state-of-the-art advancement를 본다.

따라서 연구 framing은 “내가 하고 싶은 것”이 아니라 “이 커뮤니티가 왜 지금 이걸 봐야 하는가”로 써야 한다.

2) 한 문장으로 기억되어야 한다

좋은 연구는 reviewer가 이렇게 말할 수 있어야 한다.

이 논문은 X 문제를 Y로 재정의하고, Z를 가능하게 했다.

이 문장이 안 나오면 contribution이 퍼져 있거나, 너무 작은 것이다.

3) 후속 연구가 생겨야 한다

강한 연구는 논문 이후에 질문을 만든다.

* 이 metric을 더 잘 만들 수 있나?
* 이 representation을 3D로 확장할 수 있나?
* 이 benchmark에서 다른 방법이 더 잘할 수 있나?
* 이 fabrication pipeline을 다른 material로 옮길 수 있나?
* 이 user behavior가 다른 creative domain에서도 나타나나?

후속 질문이 자연스럽게 나오면 major paper가 될 가능성이 커진다.

4) novelty와 familiarity의 균형이 있어야 한다

너무 익숙하면 incremental이다. 너무 낯설면 이해되지 않는다. 강한 연구는 보통 familiar backbone 위에 unfamiliar twist가 있다. Bibliometric 연구에서도 높은 영향력은 익숙한 조합과 비전형적 조합이 함께 있을 때 자주 나타난다.

⸻

5. 실제 연구 주제 판정 루브릭

연구 아이디어를 잡았을 때 아래 질문에 답하면 된다.

기준	좋은 답
Problem	분야의 어떤 반복 병목을 건드리는가?
Audience	누가 이 문제를 자기 문제로 느끼는가?
Prior failure	기존 방법은 왜 못 푸는가?
New lens	기존 가정 중 무엇을 바꾸는가?
Contribution	method, system, theory, dataset, study 중 무엇인가?
Evidence	claim에 맞는 검증 방식이 있는가?
Generality	예제 하나를 넘어 어떤 class of problems에 적용되는가?
Reuse	남들이 쓸 수 있는 formulation/tool/data/protocol이 있는가?
Risk	실패하면 무엇이 실패하고, 그래도 무엇을 배울 수 있는가?
Narrative	“이 논문 이후 분야가 달라지는 점”을 한 문장으로 말할 수 있는가?

이 중 Problem, New lens, Evidence, Reuse가 약하면 major research가 되기 어렵다.

⸻

6. Graphics/HCI/Robotics 쪽에서 특히 강한 방향

네 관심사 기준으로 보면, 중요한 연구는 “fabrication tool” 자체보다 아래 쪽이 더 강하다.

강한 문제군

1. semantic motion → physical motion의 변환 문제
    같은 의미의 motion이 fabrication constraint 아래에서 어떻게 바뀌어도 되는가.
2. freeform character → actuatable mechanism abstraction
    mesh를 단순 skeleton으로 줄이는 것이 아니라, visual salience와 actuation feasibility를 같이 보존하는 문제.
3. creative intent와 physical constraint의 co-optimization
    사용자가 원하는 표현과 제작 가능한 mechanism 사이의 trade-off를 탐색 가능하게 만드는 문제.
4. fabrication-aware motion representation
    motion을 먼저 만들고 나중에 제작하는 것이 아니라, motion representation 자체가 joint, cable, compliance, tolerance를 포함하는 문제.
5. mechanism sensemaking for non-experts
    novice가 mechanism을 이해하지 못하는 문제를 UI 문제가 아니라 representation/learning-scaffold 문제로 다루는 방향.

이 방향들은 단순 응용이 아니라, Graphics/HCI/Robotics 사이의 공통 병목을 건드린다.

⸻

최종 기준

임팩트 있는 연구는 “새로운 기능”이 아니라 “새로운 가능성의 단위”를 만든다.

좋은 연구 주제는 다음 문장을 만족해야 한다.

이 연구가 성공하면, 사람들은 앞으로 이 문제군을 다르게 정의하고, 다르게 측정하고, 다르게 만들고, 다르게 후속 연구를 설계하게 된다.

그 수준에 못 가면 좋은 프로젝트일 수는 있지만, major research는 아니다.
