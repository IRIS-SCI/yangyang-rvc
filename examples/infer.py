"""用本仓库的模型做一次变声（需要本机已装好 RVC / Applio 环境）。

依赖的包来自你安装的 RVC 发行版（`rvc.infer.infer.VoiceConverter`），
建议在 Applio 的 venv 里运行，或者把它挂到 PYTHONPATH 上。

用法：
    python examples/infer.py --input in.wav --output out.wav
    python examples/infer.py --input in.wav --output out.wav --pitch +12 --index-rate 1.0
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="源音频（任意人声，wav/mp3/flac 都行）")
    ap.add_argument("--output", default="out.wav")
    ap.add_argument("--model", default=os.path.join("models", "yangyang_v3_48k.pth"))
    ap.add_argument("--index", default=os.path.join("models", "yangyang_v3_48k.index"))
    ap.add_argument("--pitch", type=int, default=0, help="变调半音：女声 0，男声 +12")
    ap.add_argument("--index-rate", type=float, default=0.75)
    ap.add_argument("--f0-method", default="rmvpe", choices=["rmvpe", "harvest", "crepe", "pm"])
    ap.add_argument("--protect", type=float, default=0.33)
    args = ap.parse_args()

    if not os.path.isfile(args.model):
        sys.exit(f"模型不存在：{args.model}（从 Releases 下载后放到 models/ 里）")

    from rvc.infer.infer import VoiceConverter  # 由你安装的 RVC/Applio 提供

    vc = VoiceConverter()
    vc.convert_audio(
        audio_input_path=args.input,
        audio_output_path=args.output,
        model_path=args.model,
        index_path=args.index if os.path.isfile(args.index) else "",
        pitch=args.pitch,
        f0_method=args.f0_method,
        index_rate=args.index_rate,
        volume_envelope=1.0,
        protect=args.protect,
        embedder_model="contentvec",
        export_format="WAV",
        sid=0,
    )
    print(f"done -> {args.output}")


if __name__ == "__main__":
    main()
