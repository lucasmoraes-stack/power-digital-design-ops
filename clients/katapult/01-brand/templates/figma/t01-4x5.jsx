const imgTemplate01FullImage4X5 = "assets/6fc00337-0966-48b4-918a-0254c2d8d830.png";
const imgPhotoFull = "assets/a6f058eb-77e9-43ed-8c45-008b02865704.png";
const imgLayer1 = "assets/a6aeedad-5e4a-4760-9e4b-e77ab63c688c.svg";

export default function Template01FullImage4X5() {
  return (
    <div className="relative size-full" data-node-id="547:1295" data-name="template-01-full-image-4x5">
      <div aria-hidden className="absolute inset-0 pointer-events-none">
        <img alt="" className="absolute max-w-none object-cover size-full" src={imgTemplate01FullImage4X5} />
        <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0" />
      </div>
      <div className="absolute h-[1350px] left-0 top-0 w-[1080px]" data-node-id="547:1296" data-name="photo-full">
        <div aria-hidden className="absolute inset-0 pointer-events-none">
          <img alt="" className="absolute max-w-none object-cover size-full" src={imgPhotoFull} />
          <div className="absolute bg-gradient-to-b from-[37.218%] from-[rgba(0,0,0,0)] inset-0 to-[122.03%] to-black" />
        </div>
      </div>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[40px] items-center left-1/2 top-[836px] w-[960px]" data-node-id="547:1297">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0.9] not-italic relative shrink-0 text-[112px] text-center text-white tracking-[-4.48px] w-[960px]" data-node-id="547:1298">
          The upgrade your kitchen deserves.
        </p>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.2] not-italic relative shrink-0 text-[40px] text-center text-white w-[960px]" data-node-id="547:1299">
          No credit needed. Just fair terms and your yes.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1300" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1300;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <div className="absolute content-stretch flex items-center justify-between left-[60px] top-[1269px] w-[960px]" data-node-id="547:1301">
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[0] not-italic relative shrink-0 text-[15px] text-white w-[512px]" data-node-id="547:1302">
          <p className="leading-[1.2] mb-0">Lease-purchase service. Total cost exceeds cash price.</p>
          <p className="leading-[1.2]">Approval required. Not available in MN, NJ, WI, WY. See katapult.com.</p>
        </div>
        <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1303" data-name="Layer_1">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
        </div>
      </div>
    </div>
  );
}