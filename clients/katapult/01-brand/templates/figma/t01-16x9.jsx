const imgTemplate01FullImage16X9 = "assets/aff9cc40-2caf-4b8d-86a0-3653e7631b6e.png";
const imgPhotoFull = "assets/e74b90fb-ea74-4bbe-8477-959476ca5ee4.png";
const imgLayer1 = "assets/53412955-7c00-472f-9fbd-ffd03cec2a13.svg";

export default function Template01FullImage16X9() {
  return (
    <div className="relative size-full" data-node-id="547:1309" data-name="template-01-full-image-16x9">
      <div aria-hidden className="absolute inset-0 pointer-events-none">
        <img alt="" className="absolute max-w-none object-cover size-full" src={imgTemplate01FullImage16X9} />
        <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0" />
      </div>
      <div className="absolute h-[1080px] left-0 top-0 w-[1920px]" data-node-id="547:1310" data-name="photo-full">
        <div aria-hidden className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 overflow-hidden">
            <img alt="" className="absolute h-[205.97%] left-0 max-w-none top-[-65.91%] w-full" src={imgPhotoFull} />
          </div>
          <div className="absolute bg-gradient-to-b from-[37.218%] from-[rgba(0,0,0,0)] inset-0 to-[122.03%] to-black" />
        </div>
      </div>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[40px] items-center left-[calc(37.5%-180px)] top-[566px] w-[960px]" data-node-id="547:1311">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0.9] not-italic relative shrink-0 text-[112px] text-center text-white tracking-[-4.48px] w-[960px]" data-node-id="547:1312">
          The upgrade your kitchen deserves.
        </p>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.2] not-italic relative shrink-0 text-[40px] text-center text-white w-[960px]" data-node-id="547:1313">
          No credit needed. Just fair terms and your yes.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1314" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1314;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <div className="absolute content-stretch flex items-center justify-between left-[60px] top-[999px] w-[960px]" data-node-id="547:1315">
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[0] not-italic relative shrink-0 text-[15px] text-white w-[512px]" data-node-id="547:1316">
          <p className="leading-[1.2] mb-0">Lease-purchase service. Total cost exceeds cash price.</p>
          <p className="leading-[1.2]">Approval required. Not available in MN, NJ, WI, WY. See katapult.com.</p>
        </div>
        <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1317" data-name="Layer_1">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
        </div>
      </div>
    </div>
  );
}