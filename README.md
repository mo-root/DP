# MA'AT

<p align="center">
  Action-conditioned world modeling for billiards and snooker using large synthetic datasets, VAE latent compression, diffusion transformers, and diffusion forcing.
</p>

<p align="center">
  <a href="MA%27AT.pdf">Current Public Paper</a> ·
  <a href="paper/MAAT_renewed_paper.pdf">Renewed Paper PDF</a> ·
  <a href="paper/main.tex">Renewed Paper Source</a> ·
  <a href="https://youtu.be/WCvdq73E8tY">YouTube Presentation</a> ·
  <a href="milestones_preview/README.md">Milestones Bundle</a>
</p>

## Overview

MA'AT is a research project on playable world models for cue-sports environments. The core question is whether an action-conditioned diffusion model can preserve enough physical structure to behave like a lightweight interactive simulator rather than just a visually plausible video predictor.

The pipeline in this repo covers:

1. Large synthetic billiards data generation with aligned actions and simulator state.
2. VAE compression into compact latent representations.
3. Latent-space diffusion-transformer world-model training.
4. Baseline versus diffusion-forcing rollout evaluation.
5. Qualitative analysis of collisions, wall bounces, identity consistency, and long-horizon stability.

## Main Result

The strongest result in the current milestone package is the long-horizon gap between single-step baseline training and diffusion forcing:

| Model | MSE@16 | MSE@32 | PSNR@16 | PSNR@32 |
| --- | ---: | ---: | ---: | ---: |
| DiT baseline | 54.023 | 318.312 | 17.133 | 14.857 |
| DiT + Diffusion Forcing | 0.763 | 0.827 | 19.447 | 19.372 |

This is why the README emphasizes milestone media rather than only static documents: the qualitative clips make the physics-consistency story much clearer.

## Visual Milestones

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>1. Data Collection</h3>
      <a href="milestones_preview/data_collection/raw_episode_s3_20s.mp4">
        <img src="assets/readme/data_collection_preview.png" alt="Data collection preview strip" />
      </a>
      <p>Three dataset lineages were built to improve coverage, diversity, and hard-contact collision behavior.</p>
      <p>
        <a href="milestones_preview/data_collection/raw_episode_s3_20s.mp4">Raw episode video</a><br/>
        <a href="milestones_preview/data_collection/generated_episode_20s.mp4">Generated episode video</a><br/>
        <a href="milestones_preview/charts/data_collection_scale_frames_millions.png">Dataset scale chart</a>
      </p>
    </td>
    <td width="50%" valign="top">
      <h3>2. VAE Latent Compression</h3>
      <a href="milestones_preview/vae/vae_latent_compare_ep0_13s.mp4">
        <img src="assets/readme/vae_latent_compare.gif" alt="VAE latent comparison" />
      </a>
      <p>The VAE stage compresses frames into a compact latent space while preserving enough information for world-model training and rollout decoding.</p>
      <p>
        <a href="milestones_preview/vae/vae_preview_60m_8s.mp4">Reconstruction video</a><br/>
        <a href="milestones_preview/vae/vae_latent_compare_ep0_13s.mp4">Latent comparison video</a><br/>
        <a href="milestones_preview/vae/vae_preview_grid_60m.png">Static reconstruction grid</a>
      </p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>3. World Model Rollouts</h3>
      <a href="milestones_preview/world_model/checkpoint_progression/checkpoint_progression_686m_to_1521m_8s.mp4">
        <img src="assets/readme/latest_rollout.gif" alt="Latest rollout preview" />
      </a>
      <p>The milestone package includes baseline-vs-DF comparisons, checkpoint progression, DDIM step tradeoffs, and longer-horizon rollouts.</p>
      <p>
        <a href="milestones_preview/world_model/baseline_vs_df/ctx8_baseline_vs_dfv0_8s.mp4">Baseline vs diffusion forcing</a><br/>
        <a href="milestones_preview/world_model/checkpoint_progression/checkpoint_progression_686m_to_1521m_8s.mp4">Checkpoint progression</a><br/>
        <a href="milestones_preview/world_model/long_rollout/long_rollout_h128_10s.mp4">Long rollout</a><br/>
        <a href="milestones_preview/world_model/ddim_steps_comparison/ddim_steps_1x4_8s.mp4">DDIM comparison</a>
      </p>
    </td>
    <td width="50%" valign="top">
      <h3>4. Distillation Preview</h3>
      <a href="milestones_preview/final_project_media/distill_20260304/rollout_compare_clip_000.mp4">
        <img src="assets/readme/distillation_compare.gif" alt="Teacher and student rollout comparison" />
      </a>
      <p>A teacher-student distillation branch is included for lower-latency interactive inference while trying to preserve rollout quality.</p>
      <p>
        <a href="milestones_preview/final_project_media/distill_20260304/preview_teacher_clip_000.mp4">Teacher preview</a><br/>
        <a href="milestones_preview/final_project_media/distill_20260304/preview_student_clip_000.mp4">Student preview</a><br/>
        <a href="milestones_preview/final_project_media/distill_20260304/rollout_compare_clip_000.mp4">Teacher vs student comparison</a>
      </p>
    </td>
  </tr>
</table>

## Metric Snapshots

<p align="center">
  <img src="assets/readme/world_model_mse.png" alt="World model MSE chart" width="48%" />
  <img src="assets/readme/world_model_psnr.png" alt="World model PSNR chart" width="48%" />
</p>

- Full charts directory: [`milestones_preview/charts/`](milestones_preview/charts/README.md)
- Full world-model media bundle: [`milestones_preview/world_model/`](milestones_preview/world_model/README.md)

## Step-by-Step Media Index

This section mirrors the actual `milestones_preview/` folder layout so someone browsing the repo can follow the project in sequence.

### `milestones_preview/data_collection/`

- [`raw_episode_s3_20s.mp4`](milestones_preview/data_collection/raw_episode_s3_20s.mp4)
- [`generated_episode_20s.mp4`](milestones_preview/data_collection/generated_episode_20s.mp4)
- [`raw_preview_strip_ep0.png`](milestones_preview/data_collection/raw_preview_strip_ep0.png)
- Folder notes: [`README.md`](milestones_preview/data_collection/README.md)

### `milestones_preview/vae/`

- [`vae_preview_60m_8s.mp4`](milestones_preview/vae/vae_preview_60m_8s.mp4)
- [`vae_latent_compare_ep0_13s.mp4`](milestones_preview/vae/vae_latent_compare_ep0_13s.mp4)
- [`vae_preview_grid_60m.png`](milestones_preview/vae/vae_preview_grid_60m.png)
- Folder notes: [`README.md`](milestones_preview/vae/README.md)

### `milestones_preview/world_model/`

- [`clip_000.mp4`](milestones_preview/world_model/clip_000.mp4)
- [`clip_001.mp4`](milestones_preview/world_model/clip_001.mp4)
- [`good-collusion example.mp4`](milestones_preview/world_model/good-collusion%20example.mp4)
- Folder notes: [`README.md`](milestones_preview/world_model/README.md)

### `milestones_preview/world_model/baseline_vs_df/`

- [`ctx8_baseline_vs_dfv0_8s.mp4`](milestones_preview/world_model/baseline_vs_df/ctx8_baseline_vs_dfv0_8s.mp4)
- Folder notes: [`README.md`](milestones_preview/world_model/baseline_vs_df/README.md)

### `milestones_preview/world_model/checkpoint_progression/`

- [`checkpoint_progression_686m_to_1521m_8s.mp4`](milestones_preview/world_model/checkpoint_progression/checkpoint_progression_686m_to_1521m_8s.mp4)
- [`joint_686m_final_8s.mp4`](milestones_preview/world_model/checkpoint_progression/joint_686m_final_8s.mp4)
- [`joint_1521m_final_8s.mp4`](milestones_preview/world_model/checkpoint_progression/joint_1521m_final_8s.mp4)
- [`joint_1521m_resume360_8s.mp4`](milestones_preview/world_model/checkpoint_progression/joint_1521m_resume360_8s.mp4)
- Folder notes: [`README.md`](milestones_preview/world_model/checkpoint_progression/README.md)

### `milestones_preview/world_model/ddim_steps_comparison/`

- [`ddim08_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim08_8s.mp4)
- [`ddim12_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim12_8s.mp4)
- [`ddim20_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim20_8s.mp4)
- [`ddim30_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim30_8s.mp4)
- [`ddim_steps_1x4_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim_steps_1x4_8s.mp4)
- [`ddim_steps_2x2_8s.mp4`](milestones_preview/world_model/ddim_steps_comparison/ddim_steps_2x2_8s.mp4)
- [`actions_timeline.png`](milestones_preview/world_model/ddim_steps_comparison/actions_timeline.png)
- Folder notes: [`README.md`](milestones_preview/world_model/ddim_steps_comparison/README.md)

### `milestones_preview/world_model/long_rollout/`

- [`long_rollout_h128_10s.mp4`](milestones_preview/world_model/long_rollout/long_rollout_h128_10s.mp4)
- Folder notes: [`README.md`](milestones_preview/world_model/long_rollout/README.md)

### `milestones_preview/latest_resume555m_preview_20260303/`

- [`clip_000.mp4`](milestones_preview/latest_resume555m_preview_20260303/clip_000.mp4)
- [`clip_001.mp4`](milestones_preview/latest_resume555m_preview_20260303/clip_001.mp4)
- [`clip_002.mp4`](milestones_preview/latest_resume555m_preview_20260303/clip_002.mp4)

### `milestones_preview/final_project_media/distill_20260304/`

- [`preview_teacher_clip_000.mp4`](milestones_preview/final_project_media/distill_20260304/preview_teacher_clip_000.mp4)
- [`preview_student_clip_000.mp4`](milestones_preview/final_project_media/distill_20260304/preview_student_clip_000.mp4)
- [`rollout_compare_clip_000.mp4`](milestones_preview/final_project_media/distill_20260304/rollout_compare_clip_000.mp4)
- [`preview_teacher_clip_000.gif`](milestones_preview/final_project_media/distill_20260304/preview_teacher_clip_000.gif)
- [`preview_student_clip_000.gif`](milestones_preview/final_project_media/distill_20260304/preview_student_clip_000.gif)
- [`rollout_compare_clip_000.gif`](milestones_preview/final_project_media/distill_20260304/rollout_compare_clip_000.gif)

### `milestones_preview/gifs for esasy/`

- [`vae_latent_compare_ep0_13s.gif`](milestones_preview/gifs%20for%20esasy/vae_latent_compare_ep0_13s.gif)
- [`latest_resume555m_clip_002.gif`](milestones_preview/gifs%20for%20esasy/latest_resume555m_clip_002.gif)

## Papers

- Current public paper: [`MA'AT.pdf`](MA%27AT.pdf)
- Renewed paper PDF: [`paper/MAAT_renewed_paper.pdf`](paper/MAAT_renewed_paper.pdf)
- Renewed paper source: [`paper/main.tex`](paper/main.tex)
- Renewed paper bibliography: [`paper/refs.bib`](paper/refs.bib)
- Lightweight PDF build script: [`paper/build_public_pdf.py`](paper/build_public_pdf.py)

The renewed paper source has been cleaned for public release and a shareable PDF has been generated for the repo. Once a full TeX toolchain is available, this can be rebuilt with richer typesetting.

## Presentation

- Full project presentation: <https://youtu.be/WCvdq73E8tY>

## Repo Layout

- `milestones_preview/`: full milestone-by-milestone media package.
- `assets/readme/`: clean preview assets used by the root README.
- `paper/`: renewed paper source bundle.
- `MA'AT.pdf`: earlier public paper already uploaded to the repo.
